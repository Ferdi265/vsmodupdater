from typing import List, Optional
from pathlib import Path
import zipfile
import json
import os

def default_vspath() -> Optional[Path]:
    home = os.getenv("HOME")
    if home is not None:
        return Path(home) / ".config" / "VintagestoryData"

    appdata = os.getenv("AppData")
    if appdata is not None:
        return Path(appdata) / "VintagestoryData"

    return None

def find_mods(vspath: Path) -> List[str]:
    return [mod for mod in os.listdir(vspath / "Mods") if mod.endswith(".zip")]

def read_modinfo(vspath: Path, name: str) -> dict:
    with zipfile.ZipFile(vspath / "Mods" / name, 'r') as z:
        modinfo_str = z.read("modinfo.json")
        return json.loads(modinfo_str)

def delete_mod(vspath: Path, name: str):
    os.unlink(vspath / "Mods" / name)

def write_mod(vspath: Path, name: str, mod: bytes):
    with open(vspath / "Mods" / name, "wb") as f:
        f.write(mod)
