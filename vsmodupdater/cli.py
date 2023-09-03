import zipfile
import sys

from . import util
from . import version
from . import api
from . import fs

def update_all():
    for mod in fs.find_mods():
        try:
            modinfo = util.CaseInsensitiveDict(fs.read_modinfo(mod))
            modid = modinfo["modid"]
            modname = modinfo["name"]
            modversion = modinfo["version"]
            print(f">> checking {modname} ({modversion}) for updates")

            api_modinfo = api.get_modinfo(modid)
            api_release = api_modinfo["mod"]["releases"][0]
            api_version = api_release["modversion"]
            api_link = api_release["mainfile"]
            api_filename = api_release["filename"]

            cmp = version.compare(modversion, api_version)
            if cmp > 0:
                print("- version newer than latest (wtf?)")
                continue
            elif cmp == 0:
                print("- up to date")
                continue
            else:
                print(f"- downloading version {api_version}")

            new_mod = api.get_mod(api_link)
            fs.delete_mod(mod)
            fs.write_mod(api_filename, new_mod)
        except Exception as e:
            print(f" - failed to update {mod}: {type(e).__name__}: {e}")

def main():
    args = sys.argv[1:]

    update_all()
