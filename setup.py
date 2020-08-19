from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = ["queue", "qtmodern.windows", "qtmodern.styles"], 
                    excludes = [],
                    includes = ["guiWindow", "checkpath"],
                    include_files = ["style.qss", "gui.ini"]
                    )

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = [Executable("main.py", base=base, icon = "Xentube.ico")]

setup(
    name='Xentube',
    version = '1.0',
    author = "XENIA",
    description = "downloads, plays, and collects YouTube videos [Python & Qt]",
    options = dict(build_exe = buildOptions),
    executables = exe
)