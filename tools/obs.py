#!/usr/bin/env python3
"""OBS app builder. We pack files, not run random code."""
import argparse
import json
import pathlib
import re
import sys
import zipfile

def manifest(root):
    p=root/"obs.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    for field in ("id","name","version","entry"):
        if not isinstance(data.get(field),str) or not data[field]:
            raise ValueError("Invalid manifest field: "+field)
    if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)+",data["id"]):
        raise ValueError("Invalid application ID")
    entry=pathlib.PurePosixPath(data["entry"])
    if entry.is_absolute() or ".." in entry.parts or not (root/entry).is_file():
        raise ValueError("Invalid entry point")
    return data

def init(name):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+",name):
        raise ValueError("Use letters, numbers, underscore or hyphen")
    root=pathlib.Path(name)
    root.mkdir(exist_ok=False)
    (root/"main.py").write_text('print("Hello from OBSIDIAN")\n',encoding="utf-8")
    (root/"obs.json").write_text(json.dumps({
        "id":"org.obsidian."+name.lower().replace("_","-"),
        "name":name,"version":"0.1.0","entry":"main.py",
        "runtime":"python3","permissions":[]},indent=2)+"\n",encoding="utf-8")
    print("Created",root)

def build(folder):
    root=pathlib.Path(folder).resolve()
    data=manifest(root)
    output=pathlib.Path.cwd()/(root.name+".obs")
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_symlink():
                raise ValueError("Symlinks are not supported")
            if p.is_file():
                z.write(p,p.relative_to(root).as_posix())
    print("Created",output,"for",data["id"])

# Heads up: inspection reads metadata only. No mystery code gets launched.
def inspect(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if "obs.json" not in names or len(names)!=len(set(names)):
            raise ValueError("Invalid package")
        for n in names:
            p=pathlib.PurePosixPath(n)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError("Unsafe package path")
        data=json.loads(z.read("obs.json"))
        print(json.dumps(data,indent=2))
        print("Archive entries:",len(names))
        print("Signature: NOT VERIFIED (experimental format)")

def main():
    p=argparse.ArgumentParser(prog="obs")
    sub=p.add_subparsers(dest="cmd",required=True)
    for cmd,arg in (("init","name"),("build","folder"),("inspect","package")):
        sub.add_parser(cmd).add_argument(arg)
    a=p.parse_args()
    try:
        if a.cmd=="init":init(a.name)
        elif a.cmd=="build":build(a.folder)
        else:inspect(a.package)
    except (ValueError,OSError,zipfile.BadZipFile,KeyError) as e:
        p.exit(1,"OBS error: "+str(e)+"\n")
if __name__=="__main__":main()
