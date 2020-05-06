import cx_Freeze
import sys

base = None

if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name="Visage Differentiation",
    options={"build_exe": {"optimize": 2}},
    version="1.0.0",
    description="Identifies unknown visages.",
    executables=[cx_Freeze.Executable("visage_differentiation/application.py", base=base)]
)
