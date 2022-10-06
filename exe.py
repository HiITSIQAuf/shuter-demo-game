from http.server import executable
from unicodedata import name
import main
from cx_Freeze import *
import sys

sys.argv.append("build")

setup(
    name = "Hello",
    options = {"build_exe": {"packages": ['ursina']}},
    executables = [
        Executable(
            "main.py"
        )
    ]
)