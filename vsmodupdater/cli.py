from typing import Tuple
from pathlib import Path
from argparse import ArgumentParser, Namespace
import traceback
import argparse
import sys

from . import util
from . import version
from . import api
from . import fs

def update_all(args: Namespace):
    for mod in fs.find_mods(args.vs_dir):
        try:
            modinfo = fs.read_modinfo(args.vs_dir, mod)
            modid = modinfo["modid"]
            modname = modinfo["name"]
            modversion = modinfo["version"]
            print(f">> {modname:30} | current: {modversion:8} | ", end="", flush=True)

            api_modinfo = api.get_modinfo(args.moddb_url, modid)
            api_release = api_modinfo["mod"]["releases"][0]
            api_version = api_release["modversion"]
            api_link = api_release["mainfile"]
            print(f"latest: {api_version:8} | ", end="", flush=True)

            cmp = version.compare(modversion, api_version)
            if cmp > 0 and not args.force:
                print("version newer than latest? WTF?")
                continue
            elif cmp == 0 and not args.force:
                print("up to date")
                continue
            else:
                print(f"downloading | ", end="", flush=True)

            new_mod = api.get_file(args.moddb_url, api_link)
            new_filename = f"{modid}_{api_version}.zip"

            if args.dry_run:
                print("skipping update")
            else:
                fs.delete_mod(args.vs_dir, mod)
                fs.write_mod(args.vs_dir, new_filename, new_mod)
                print("updated")
        except Exception as e:
            print()
            print(f" - failed to update {mod}: {type(e).__name__}: {e}")
            print(traceback.format_exc())

def parse_args() -> Tuple[ArgumentParser, Namespace]:
    ap = argparse.ArgumentParser("vsmodupdater", description="A tool for updating VintageStory mods")

    ap.add_argument("-a", "--all", action="store_true", help="update all mods")
    ap.add_argument("-f", "--force", action="store_true", help="force redownload even if up to date")
    ap.add_argument("-d", "--dry-run", action="store_true", help="don't update even if out of date")
    ap.add_argument("-M", "--moddb-url", action="store", type=str, help="VintageStory ModDB API URL", default=api.default_moddburl())
    ap.add_argument("-V", "--vs-dir", action="store", type=Path, help="VintageStory data directory", default=fs.default_vspath())

    return ap, ap.parse_args()

def main():
    ap, args = parse_args()

    if args.vs_dir is None:
        print("error: VintageStory data directory unknown, please specify with --vs-dir")
        return

    try:
        if args.all:
            update_all(args)
        else:
            ap.print_help()
    except KeyboardInterrupt:
        print()
