# Dynaframe-Testing

Test store for DynaframePro plugins. New plugins and versions land here first and move to
[Jan's Store](https://github.com/Archonw/Dynaframe-Stuff) once they work.

Store address for the frame:

    https://raw.githubusercontent.com/Archonw/Dynaframe-Testing/main/DynaframPro/Jans-store/catalog.json

Same layout as Dynaframe-Stuff: `catalog.json` lists the packs, `plugin_packs/<id>/` holds the ZIP and `thumb.webp`.
`size` is the ZIP size in bytes, `checksum` its SHA-256.

To publish a pack: copy its folder to Dynaframe-Stuff and move its entry into that store's `catalog.json`.
