import traceback
import argparse
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
            print(f">> {modname:30} | current: {modversion:8} | ", end="", flush=True)

            api_modinfo = api.get_modinfo(modid)
            api_release = api_modinfo["mod"]["releases"][0]
            api_version = api_release["modversion"]
            api_link = api_release["mainfile"]
            api_filename = api_release["filename"]
            print(f"latest: {api_version:8} | ", end="", flush=True)

            cmp = version.compare(modversion, api_version)
            if cmp > 0:
                print("version newer than latest? WTF?")
                continue
            elif cmp == 0:
                print("up to date")
                continue
            else:
                print(f"downloading | ", end="", flush=True)

            new_mod = api.get_mod(api_link)
            fs.delete_mod(mod)
            fs.write_mod(api_filename, new_mod)
            print("updated")
        except Exception as e:
            print()
            print(f" - failed to update {mod}: {type(e).__name__}: {e}")
            print(traceback.format_exc())

def parse_args():
    ap = argparse.ArgumentParser("vsmodupdater", description="A tool for updating Vintagestory mods")

    ap.add_argument("--moddb-url", action="store", type=str, help="VintageStory ModDB API URL", default=api.BASEURL)
    ap.add_argument("--mod-dir", action="store", type=str, help="VintageStory mods directory", default=fs.MODPATH)
    ap.add_argument("-a", "--all", action="store_true", help="update all mods")

    return ap, ap.parse_args()

def main():
    ap, args = parse_args()

    api.BASEURL = args.moddb_url
    fs.MODPATH = args.mod_dir

    if args.all:
        try:
            update_all(args)
        except KeyboardInterrupt:
            print()
    else:
        ap.print_help()
