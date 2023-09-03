from typing import List, Dict, Optional
from pathlib import Path
import zipfile
import json
import os

from . import util

def default_vspath(prefer_flatpak: bool = False) -> Optional[Path]:
    paths = [
        ("XDG_CONFIG_HOME", Path("VintagestoryData")),
        ("HOME", Path(".config") / "VintagestoryData"),
        ("AppData", Path("VintagestoryData")),
    ]

    flatpak_path = ("HOME", Path(".var") / "app" / "at.vintagestory.VintageStory" / "config" / "VintagestoryData")
    paths.insert(0 if prefer_flatpak else len(paths), flatpak_path)

    for envvar, fpath in paths:
        var = os.getenv(envvar)
        if var is None:
            continue

        path = Path(var) / fpath
        if not path.exists():
            continue

        return path

    return None

def find_mods(vspath: Path) -> List[str]:
    if not (vspath / "Mods").exists():
        return []

    return [mod for mod in os.listdir(vspath / "Mods") if mod.endswith(".zip")]

def find_mods_by_id(vspath: Path) -> Dict[str, str]:
    mods_by_id = {}
    for mod in find_mods(vspath):
        try:
            modinfo = read_modinfo(vspath, mod)
            modid = modinfo["modid"]
            mods_by_id[modid] = mod
        except Exception:
            pass

    return mods_by_id

def read_modinfo(vspath: Path, name: str) -> dict:
    with zipfile.ZipFile(vspath / "Mods" / name, 'r') as z:
        modinfo_str = z.read("modinfo.json")
        return util.CaseInsensitiveDict(json.loads(modinfo_str))

def delete_mod(vspath: Path, name: str):
    os.unlink(vspath / "Mods" / name)

def write_mod(vspath: Path, name: str, mod: bytes):
    with open(vspath / "Mods" / name, "wb") as f:
        f.write(mod)
