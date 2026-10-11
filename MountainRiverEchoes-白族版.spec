# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['musicdl', 'musicdl.musicdl', 'orjson', 'json_repair', 'aigpy', 'cryptography', 'fake_useragent', 'ytmusicapi', 'm3u8', 'mutagen', 'tinytag', 'curl_cffi', 'lxml', 'bleach', 'emoji', 'rich', 'prettytable', 'tabulate', 'prompt_toolkit', 'filetype', 'puremagic', 'platformdirs', 'brotli', 'pathvalidate', 'typing_extensions', 'yt_dlp']
hiddenimports += collect_submodules('musicdl')


a = Analysis(
    ['webui/mountainriverechoes.py'],
    pathex=['C:/Users/HUAWEI/WorkBuddy/2026-10-11-17-52-29/mountainriverechoes'],
    binaries=[],
    datas=[('webui/templates', 'webui/templates'), ('webui/ethnos_cache', 'webui/ethnos_cache'), ('webui/ui_state.json', 'webui'), ('musicdl/modules/wvds', 'musicdl/modules/wvds')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['av'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MountainRiverEchoes-白族版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MountainRiverEchoes-白族版',
)
