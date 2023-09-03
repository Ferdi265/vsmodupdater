from typing import List
import zipfile
import json
import os

MODPATH = os.environ["HOME"] + "/.config/VintagestoryData/Mods"

def find_mods() -> List[str]:
    return [mod for mod in os.listdir(MODPATH) if mod.endswith(".zip")]

def read_modinfo(name: str) -> dict:
    with zipfile.ZipFile(MODPATH + "/" + name, 'r') as z:
        modinfo_str = z.read("modinfo.json")
        return json.loads(modinfo_str)

def delete_mod(name: str):
    os.unlink(MODPATH + "/" + name)

def write_mod(name: str, mod: bytes):
    with open(MODPATH + "/" + name, "wb") as f:
        f.write(mod)
