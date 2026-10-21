#!/usr/bin/env python3
"""Raeumt Reste deinstallierter Integrationen auf: DynaFrame loescht beim Deinstallieren nur
die Szene und den Store-Eintrag und deaktiviert das Plugin, laesst aber den Plugin-Ordner und
einen leeren dynamic-packages/<id>-Ordner stehen. Ohne Argument nur Anzeige, mit 'los' wird geloescht."""
import json, os, shutil, sys, urllib.request

HOME = os.path.expanduser("~")
DYN = os.path.join(HOME, ".local/share/dfr/dynamic-packages")
PLUG = os.path.join(HOME, ".local/share/dfr/plugins")

with urllib.request.urlopen("http://localhost/Store/GetInstalledPacks", timeout=20) as r:
    installed = {p["packId"] for p in json.load(r).get("packs", [])}

# Plugin-Ordner nach Store-Pack-ID (steht in .dynaframe-install.json)
plugins = {}
for name in sorted(os.listdir(PLUG)):
    path = os.path.join(PLUG, name)
    try:
        info = json.load(open(os.path.join(path, ".dynaframe-install.json")))
        enabled = json.load(open(os.path.join(path, "manifest.json"))).get("Enabled", True)
    except Exception:
        continue
    if info.get("storePackId"):
        plugins.setdefault(info["storePackId"], []).append((path, enabled))

todo = []
for pid in sorted(os.listdir(DYN)):
    d = os.path.join(DYN, pid)
    if not os.path.isdir(d) or pid in installed or os.listdir(d):
        continue  # noch installiert oder es liegt noch eine Version darin
    todo.append(d)
    for path, enabled in plugins.get(pid, []):
        if enabled:
            print(f"UEBERSPRUNGEN (Plugin noch aktiv): {path}")
        else:
            todo.append(path)

if not todo:
    print("Nichts aufzuraeumen.")
for path in todo:
    print(("loesche  " if sys.argv[1:] == ["los"] else "wuerde loeschen  ") + path)
    if sys.argv[1:] == ["los"]:
        shutil.rmtree(path, ignore_errors=True)
if todo and sys.argv[1:] != ["los"]:
    print("\nNur Anzeige. Zum Loeschen: python3 integrations-reste-aufraeumen.py los")
elif todo:
    print("\nFertig. Jetzt DynaFrame neu starten (oder den Rahmen) und die Store-Seite neu laden.")
