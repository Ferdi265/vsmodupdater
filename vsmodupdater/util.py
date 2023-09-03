from typing import IO, Any
from pathlib import Path
import sys

class CaseInsensitiveDict(dict):
    def __init__(self, *args, **kwargs):
        orig = dict(*args, **kwargs)
        new = {key.lower(): value for key, value in orig.items()}
        super().__init__(new)

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

def open_or_stdio(name: str | Path, mode: str) -> IO[Any]:
    if str(name) == "-":
        if mode == "r":
            return sys.stdin
        elif mode == "w":
            return sys.stdout

    return open(name, mode)
