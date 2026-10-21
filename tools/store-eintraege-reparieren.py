#!/usr/bin/env python3
"""Traegt Jans Packs, die auf dem Rahmen liegen, aber im Store-Verzeichnis fehlen,
wieder ein (POST /Store/MarkPackInstalled). Ohne Argument nur Anzeige, mit 'los' wird eingetragen."""
import json, os, sys, urllib.request

BASE = "http://localhost"
HOME = os.path.expanduser("~")
DYN = os.path.join(HOME, ".local/share/dfr/dynamic-packages")
PLUG = os.path.join(HOME, ".local/share/dfr/plugins")
STORES = [
    "https://raw.githubusercontent.com/Archonw/Dynaframe-Stuff/main/DynaframPro/Jans-store/catalog.json",
    "https://raw.githubusercontent.com/Archonw/Dynaframe-Testing/main/DynaframPro/Jans-store/catalog.json",
]
# Plugin-Packs (Typ plugin) und ihr Ordner unter plugins/
PLUGIN_DIRS = {"immich": "ImmichSlideshow", "jellyfin-now-playing": "JellyfinNowPlaying",
               "playlist-button": "PlaylistButtonPlugin", "webpage-button": "WebPageButtonPlugin"}

def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)

def vkey(v):
    return [int(x) if x.isdigit() else 0 for x in v.split(".")]

installed = {p["packId"] for p in get(BASE + "/Store/GetInstalledPacks").get("packs", [])}
entries = {}
for url in STORES:  # Stuff zuerst; Testing nur fuer Packs, die es oeffentlich nicht gibt
    try:
        for p in get(url)["packs"]:
            entries.setdefault(p["id"], []).append(dict(p, sourceStore=url))
    except Exception as e:
        print("Katalog nicht ladbar:", url, e)
packs = {}
for pid, lst in entries.items():
    # Liegt das Pack als Integration auf dem Rahmen (z. B. Jellyfin 0.4.x), den Integrations-Eintrag nehmen
    if os.path.isdir(os.path.join(DYN, pid)):
        lst = [p for p in lst if p["type"] == "integration"] or lst
    packs[pid] = lst[0]

todo = []
for pid, p in packs.items():
    if pid in installed:
        continue
    if p["type"] == "integration" and os.path.isdir(os.path.join(DYN, pid)):
        versions = sorted((d for d in os.listdir(os.path.join(DYN, pid))
                           if os.path.isdir(os.path.join(DYN, pid, d))), key=vkey)
        if not versions:
            continue
        todo.append((p, versions[-1], os.path.join(DYN, pid, versions[-1])))
    elif p["type"] == "plugin" and pid in PLUGIN_DIRS and os.path.isdir(os.path.join(PLUG, PLUGIN_DIRS[pid])):
        path = os.path.join(PLUG, PLUGIN_DIRS[pid])
        version = p["version"]
        try:
            version = json.load(open(os.path.join(path, "manifest.json"))).get("Version") or version
        except Exception:
            pass
        todo.append((p, version, path))

if not todo:
    print("Nichts zu tun: alle vorhandenen Packs sind im Store eingetragen.")
for p, version, path in todo:
    print(f"{p['id']:28} {p['type']:12} {version:10} {path}")
    if sys.argv[1:] == ["los"]:
        body = json.dumps({"PackId": p["id"], "Type": p["type"], "Title": p["title"],
                           "Author": p.get("author", "Jan"), "Version": version,
                           "SourceStore": p["sourceStore"], "InstallPath": path,
                           "Checksum": p.get("checksum", ""), "Size": p.get("size_bytes") or p.get("size") or 0}).encode()
        req = urllib.request.Request(BASE + "/Store/MarkPackInstalled", data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                print("   ->", r.read().decode()[:200])
        except Exception as e:
            print("   -> FEHLER", e)
if todo and sys.argv[1:] != ["los"]:
    print("\nNur Anzeige. Zum Eintragen: python3 store-eintraege-reparieren.py los")
