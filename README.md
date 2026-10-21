# Dynaframe-Testing

Test store for DynaframePro plugins. New plugins and versions land here first and move to
[Jan's Store](https://github.com/Archonw/Jans-DynaframePro-Store) once they work.

Store address for the frame:

    https://raw.githubusercontent.com/Archonw/Dynaframe-Testing/main/DynaframPro/Jans-store/catalog.json

`catalog.json` lists the packs, `plugin_packs/<id>/` holds the ZIP and `thumb.webp`. Use `"type": "plugin"` for a plain plugin ZIP (manifest.json at the root) and `"type": "integration"` for a scene+plugin bundle with `dynaframe-package.json`; with the wrong type the Store installs the pack but shows "Error".
`size` is the ZIP size in bytes, `checksum` its SHA-256.

To publish a pack: copy its folder to [Jans-DynaframePro-Store](https://github.com/Archonw/Jans-DynaframePro-Store) (`plugin_packs/<id>/`, the catalog sits at the root there, so paths drop `DynaframPro/Jans-store/`) and copy its entry into that store's `catalog.json` with a higher version. Links inside the packs must point to Jans-DynaframePro-Store. Details in [CLAUDE.md](CLAUDE.md). Dynaframe-Stuff no longer holds a store.
