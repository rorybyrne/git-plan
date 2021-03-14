from pathlib import Path

VERSION = {}
try:
    with open(Path(__file__).parent / "_version.py", "rb") as file:
        exec(file.read(), VERSION)
except FileNotFoundError:
    VERSION["__version__"] = "dev"

__version__ = VERSION["__version__"]
