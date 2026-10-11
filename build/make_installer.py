import os
import sys
import time
import shutil
import zipfile
import tempfile
import subprocess
import traceback
from pathlib import Path

APP_NAME = "MountainRiverEchoes-白族版"
ZIP = "app.zip"


def resource(name):
    # PyInstaller 冻结后资源在 sys._MEIPASS; 未冻结时取脚本同目录
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    p = Path(base) / name
    # 兜底: 若被 --add-data 误放进同名子目录(如 app.zip/app.zip), 自动取内层文件
    if p.is_dir():
        inner = p / name
        if inner.is_file():
            return inner
    return p


def pause():
    try:
        input("按回车退出...")
    except Exception:
        pass


def main():
    # 让中文在 Windows 控制台正确显示
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        os.system("chcp 65001 >nul 2>&1")
    except Exception:
        pass

    try:
        default = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / APP_NAME
        target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default

        zip_path = resource(ZIP)
        if not zip_path.exists():
            print(f"[错误] 安装包缺失: {zip_path}\n请把 app.zip 与本安装程序放在同一目录, 或重新下载完整安装包。")
            pause()
            return

        # 先拷到普通临时文件再打开, 避免 _MEIPASS 临时目录的读取限制
        tmp_zip = Path(tempfile.gettempdir()) / "mre_app_tmp.zip"
        last_err = None
        for attempt in range(5):
            try:
                shutil.copyfile(zip_path, tmp_zip)
                last_err = None
                break
            except Exception as e:
                last_err = e
                time.sleep(0.6)
        if last_err is not None:
            print(f"[错误] 无法读取内嵌安装包: {last_err}")
            print(f"(源路径: {zip_path})")
            pause()
            return

        print("=" * 48)
        print("  山河回响 · 白族版  安装程序")
        print("=" * 48)
        print(f"安装位置: {target}")
        target.mkdir(parents=True, exist_ok=True)

        print("正在解压(首次稍慢, 请稍候)...")
        try:
            with zipfile.ZipFile(tmp_zip, "r") as z:
                z.extractall(target)
        except Exception as e:
            print("[解压出错]", e)
            traceback.print_exc()
            pause()
            return

        exe = target / APP_NAME / (APP_NAME + ".exe")
        if not exe.exists():
            print(f"[错误] 解压后未找到主程序: {exe}")
            pause()
            return

        # 桌面快捷方式(优先 .lnk, 失败则退化为 .bat)
        desktop = Path.home() / "Desktop"
        lnk = desktop / f"{APP_NAME}.lnk"
        shortcut_info = ""
        try:
            ps = (
                "$ws=New-Object -ComObject WScript.Shell; "
                f'$s=$ws.CreateShortcut(\"{lnk}\"); '
                f'$s.TargetPath=\"{exe}\"; '
                f'$s.WorkingDirectory=\"{target / APP_NAME}\"; '
                '$s.Description="山河回响·白族版 民族音乐"; '
                "$s.Save()"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, capture_output=True)
            shortcut_info = f"桌面快捷方式: {lnk}"
        except Exception:
            bat = desktop / f"{APP_NAME}.bat"
            bat.write_text('@echo off\nstart "" "%~dp0MountainRiverEchoes-白族版\\MountainRiverEchoes-白族版.exe"\n', encoding="utf-8")
            shortcut_info = f"桌面启动脚本: {bat}"

        print("-" * 48)
        print("安装完成!")
        print(f"- 主程序: {exe}")
        print(f"- {shortcut_info}")
        print("-" * 48)
        print("双击桌面快捷方式即可打开本软件: 它会自动启动本地服务,")
        print("并在浏览器打开  http://127.0.0.1:8766  (白族音乐 538 首)。")
    except Exception as e:
        print("[安装出错]", e)
        traceback.print_exc()
    finally:
        if getattr(sys, "frozen", False):
            pause()


if __name__ == "__main__":
    main()
