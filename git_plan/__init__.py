from pathlib import Path

VERSION = {}
try:
    with open(Path(__file__).parent / "_version", "r") as file:
        VERSION["__version__"] = file.read().strip()
except FileNotFoundError:
    VERSION["__version__"] = "dev"

__version__ = VERSION["__version__"]
