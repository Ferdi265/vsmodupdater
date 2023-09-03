import requests as rq

BASEURL = "https://mods.vintagestory.at"

def get_modinfo(mod: str) -> dict:
    return rq.get(BASEURL + "/api/mod/" + mod).json()

def get_mod(link: str) -> bytes:
    return rq.get(BASEURL + "/" + link).content
