"""Apply a small compatibility shim to the installed `construct` package.

Why this exists
---------------
`pywidevine` (used by musicdl's Apple Music source) depends on `pymp4`, which was
written against the construct 2.9 API. PyPI now ships construct 2.10+, which
removed/renamed several of those APIs (`String`, `Embedded`, `EmbeddedBitStruct`,
`BoundBytesIO`) and made `encoding` mandatory on `CString`/`PascalString`/
`GreedyString`, and swapped the `Const` argument order. Without this shim,
`import musicdl` fails with TypeError/NameError and the web UI cannot start.

This script appends a self-contained shim to `construct/__init__.py` inside the
project virtualenv. It is idempotent: running it twice is harmless.

Usage
-----
    venv\\Scripts\\python.exe patch_construct.py
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
VENVS = [
    ROOT / "venv" / "Lib" / "site-packages" / "construct" / "__init__.py",   # Windows
    ROOT / "venv" / "lib" / "python3.13" / "site-packages" / "construct" / "__init__.py",
]
MARKER = "# compat shim: construct 2.9 API surface"

SHIM = '''

#===============================================================================
# compat shim: construct 2.9 API surface still used by pymp4 / pywidevine
# (Apple Music / Widevine code path). Restores names and signatures that
# construct 2.10 dropped or made stricter, so those old parsers keep importing.
#===============================================================================
from construct import core as _core
import io as _io


def String(length, encoding="utf8", padchar=b"\\x00", paddir="right"):
    """construct 2.9 String(length, encoding, padchar, paddir)."""
    if isinstance(padchar, bytes):
        padchar = padchar.decode("latin1")

    class _StringCompat(_core.Adapter):
        def __init__(self):
            super().__init__(_core.FixedSized(length, _core.GreedyString(encoding=encoding)))

        def _decode(self, obj, context, path):
            return obj.rstrip(padchar) if paddir == "right" else obj.lstrip(padchar)

        def _encode(self, obj, context, path):
            return obj

    return _StringCompat()


def Embedded(subcon):
    """2.9 inlined a subcon into its parent struct; 2.10 nests instead."""
    return subcon


def EmbeddedBitStruct(*fields, **kwargs):
    return _core.BitStruct(*fields, **kwargs)


class BoundBytesIO(_io.BytesIO):
    """2.9 construct.lib.BoundBytesIO: a length-limited view over a stream."""

    def __init__(self, stream, size=None):
        data = stream.read(size) if size is not None else stream.read()
        super().__init__(data)


def _compat_const(value, subcon=None):
    """Accept 2.9 order Const(subcon, value) as well as 2.10 Const(value, subcon)."""
    if subcon is not None and isinstance(value, _core.Construct):
        value, subcon = subcon, value
    return _core.Const(value) if subcon is None else _core.Const(value, subcon)


def _compat_default_encoding(orig, name):
    """2.9 defaulted encoding='utf8'; 2.10 requires it explicitly."""
    def wrapper(*args, **kwargs):
        if "encoding" not in kwargs:
            last_is_encoding = bool(args) and isinstance(args[-1], str)
            if not last_is_encoding:
                if name == "PascalString":
                    if len(args) < 2:
                        kwargs["encoding"] = "utf8"
                elif not args:
                    kwargs["encoding"] = "utf8"
        return orig(*args, **kwargs)
    return wrapper


Const = _compat_const
CString = _compat_default_encoding(_core.CString, "CString")
PascalString = _compat_default_encoding(_core.PascalString, "PascalString")
GreedyString = _compat_default_encoding(_core.GreedyString, "GreedyString")

__all__ += ['String', 'Embedded', 'EmbeddedBitStruct', 'BoundBytesIO']
'''


def find_target():
    for p in VENVS:
        if p.exists():
            return p
    # fall back: any construct package inside the project venv
    for p in (ROOT / "venv").rglob("construct/__init__.py"):
        return p
    return None


def main():
    target = find_target()
    if target is None:
        print("[patch_construct] 未找到 venv 中的 construct 包，请先创建虚拟环境并安装依赖。")
        return 1

    text = target.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"[patch_construct] 已打过补丁，跳过：{target}")
        return 0

    target.write_text(text.rstrip() + "\n" + SHIM, encoding="utf-8")
    print(f"[patch_construct] 已写入兼容层：{target}")
    print("[patch_construct] 现在应能正常 import musicdl。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
