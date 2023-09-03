import requests as rq

def default_moddburl() -> str:
    return "https://mods.vintagestory.at"

def get_modinfo(moddburl: str, mod: str) -> dict:
    return rq.get(f"{moddburl}/api/mod/{mod}").json()

def get_file(moddburl: str, link: str) -> bytes:
    return rq.get(f"{moddburl}/{link}").content
