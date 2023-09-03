from typing import Tuple, Dict
from pathlib import Path
from argparse import ArgumentParser, Namespace
import traceback
import argparse
import sys

from . import util
from . import version
from . import api
from . import fs

def install_mods(args: Namespace):
    existing_mods = fs.find_mods_by_id(args.vs_dir)
    for modid in args.install:
        try:
            api_modinfo = api.get_modinfo(args.moddb_url, modid)
            api_modname = api_modinfo["mod"]["name"]
            api_release = api_modinfo["mod"]["releases"][0]
            api_version = api_release["modversion"]
            api_link = api_release["mainfile"]
            print(f">> {api_modname:30} | id: {modid:30} | ", end="", flush=True)

            if modid in existing_mods:
                modinfo = fs.read_modinfo(args.vs_dir, existing_mods[modid])
                modversion = modinfo["version"]
            else:
                modversion = "none"

            print(f"current: {modversion:8} | latest: {api_version:8} | ", end="", flush=True)

            if modversion != "none":
                cmp = version.compare(modversion, api_version)
                if cmp > 0 and not args.force:
                    print("version newer than latest? WTF?")
                    continue
                elif cmp == 0 and not args.force:
                    print("up to date")
                    continue

            print(f"downloading | ", end="", flush=True)
            new_mod = api.get_file(args.moddb_url, api_link)
            new_filename = f"{modid}_{api_version}.zip"

            if args.dry_run:
                print("skipping install")
            else:
                if modid in existing_mods:
                    fs.delete_mod(args.vs_dir, existing_mods[modid])
                fs.write_mod(args.vs_dir, new_filename, new_mod)
                print("installed")
        except Exception as e:
            print()
            print(f" - failed to install {modid}: {type(e).__name__}: {e}")
            print(traceback.format_exc())

def install_mods_file(args: Namespace):
    with util.open_or_stdio(args.install_file, "r") as f:
        args.install = [mod for mod in f.read().split("\n") if len(mod) != 0]

    install_mods(args)

def remove_mods(args: Namespace):
    existing_mods = fs.find_mods_by_id(args.vs_dir)
    for modid in args.remove:
        try:
            if modid not in existing_mods:
                continue

            modinfo = fs.read_modinfo(args.vs_dir, existing_mods[modid])
            modname = modinfo["name"]
            modversion = modinfo["version"]
            print(f">> {modname:30} | id: {modid:30} | current: {modversion:8} | removing | ", end="", flush=True)

            if args.dry_run:
                print("skipping remove")
            else:
                fs.delete_mod(args.vs_dir, existing_mods[modid])
                print("removeed")
        except Exception as e:
            print()
            print(f" - failed to remove {modid}: {type(e).__name__}: {e}")
            print(traceback.format_exc())

def remove_mods_file(args: Namespace):
    with util.open_or_stdio(args.remove_file, "r") as f:
        args.remove = [mod for mod in f.read().split("\n") if len(mod) != 0]

    remove_mods(args)

def dump_mods(args: Namespace):
    existing_mods = fs.find_mods_by_id(args.vs_dir)
    with util.open_or_stdio(args.dump_file, "w") as f:
        for modid in existing_mods.keys():
            f.write(f"{modid}\n")

def update_all(args: Namespace):
    for mod in fs.find_mods(args.vs_dir):
        try:
            modinfo = fs.read_modinfo(args.vs_dir, mod)
            modid = modinfo["modid"]
            modname = modinfo["name"]
            modversion = modinfo["version"]
            print(f">> {modname:30} | id: {modid:30} | current: {modversion:8} | ", end="", flush=True)

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

    ap.add_argument("-i", "--install", nargs="+", action="store", type=str, help="install mods with the given ids")
    ap.add_argument("-I", "--install-file", action="store", type=Path, help="install mods from the given file")
    ap.add_argument("-r", "--remove", nargs="+", action="store", type=str, help="remove mods with the given ids")
    ap.add_argument("-R", "--remove-file", action="store", type=Path, help="remove mods from the given file")
    ap.add_argument("-D", "--dump-file", action="store", type=Path, help="dump installed mod ids to the given file")
    ap.add_argument("-f", "--force", action="store_true", help="force redownload even if up to date")
    ap.add_argument("-d", "--dry-run", action="store_true", help="don't update even if out of date")
    ap.add_argument("-M", "--moddb-url", action="store", type=str, help="VintageStory ModDB API URL")
    ap.add_argument("-V", "--vs-dir", action="store", type=Path, help="VintageStory data directory")
    ap.add_argument("-F", "--prefer-flatpak", action="store_true", help="prefer the config directory for the VintageStory Flatpak over native")

    return ap, ap.parse_args()

def main():
    ap, args = parse_args()

    if args.moddb_url is None:
        args.moddb_url = api.default_moddburl()

    if args.vs_dir is None:
        args.vs_dir = fs.default_vspath(prefer_flatpak = args.prefer_flatpak)
    if args.vs_dir is None:
        print("error: VintageStory data directory not found, please specify with --vs-dir")
        return

    try:
        if args.install is not None:
            install_mods(args)
        elif args.install_file is not None:
            install_mods_file(args)
        elif args.remove is not None:
            remove_mods(args)
        elif args.remove_file is not None:
            remove_mods_file(args)
        elif args.dump_file is not None:
            dump_mods(args)
        else:
            update_all(args)
    except KeyboardInterrupt:
        print()
