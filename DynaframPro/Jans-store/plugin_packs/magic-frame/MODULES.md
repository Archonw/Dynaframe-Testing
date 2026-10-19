# Writing a Magic Frame module

A Magic Frame module is a folder with up to four files:

```
magicframe/
  module.json   what the module is called and which settings it has (required)
  module.js     draws the module in the scene (required)
  module.css    extra styles (optional)
  fetch.py      fetches data on the frame (optional)
```

Magic Frame finds modules in two places and checks again every minute:

1. **Inside any other installed DynaFrame plugin** that has a `magicframe/` folder. So a module can be shipped through any plugin store as a normal (tiny) plugin. See the example `MagicFramePegelstand` in Jan's store: its `plugin.py` only calls `ready()` and idles.
2. **From a ZIP link** pasted on the Magic Frame page ("Add-on modules"). The ZIP contains the files above, at the top level or in one folder. They are unpacked to Magic Frame's own data folder.

After that, the module appears under **Add module** like a built-in one, and its settings form is generated from `module.json`.

## module.json

```json
{
  "type": "pegelstand",
  "name": {"de": "Pegelstand", "en": "River level", "es": "Nivel del río"},
  "description": {"de": "…", "en": "…", "es": "…"},
  "version": "1.0.0",
  "author": "Your name",
  "url": "https://github.com/you/your-module",
  "region": "top_right",
  "script": "module.js",
  "style": "module.css",
  "fetch": "fetch.py",
  "every": 900,
  "visibleOnly": false,
  "place": false,
  "fields": [
    {"key": "station", "kind": "text", "default": "MAINZ",
     "label": {"de": "Pegel", "en": "Gauge", "es": "Estación"},
     "hint": {"en": "All gauges: pegelonline.wsv.de"}}
  ]
}
```

- `type`: unique id, lowercase letters, digits, `.`, `_`, `-` (2–48 chars). Use a prefix such as `yourname.weather` to avoid clashes. Built-in types (`clock`, `weather`, `forecast`, `rain`, `calendar`, `news`, `departures`, `compliments`, `warnings`, `homeassistant`, `webpage`) are taken.
- Texts (`name`, `description`, `label`, `hint`, option labels) are a string or `{"de", "en", "es"}`; missing languages fall back to English.
- `region`: where the module lands when added: `top_bar`, `top_left`, `top_center`, `top_right`, `middle_left`, `middle_center`, `middle_right`, `bottom_left`, `bottom_center`, `bottom_right`, `bottom_bar`.
- `every`: seconds between fetches (30 to 86400). `visibleOnly`: only fetch while the scene is on screen (for data that changes by the minute). `place`: the module needs the location set on the page (`ctx["lat"]`, `ctx["lon"]`).
- `fields[].kind`: `text`, `textarea`, `number` (with `min`/`max`), `bool`, `select` (with `options: [{"value", "label"}]`), `secret` (passwords and tokens: never sent to the scene or back to the page), `stop` (a public transport stop picked via search). `showIf: {"otherKey": "value"}` shows a field only for that value. Every module also gets a `header` field automatically.

## module.js

```js
(function () {
  const { esc, t } = window.MagicFrame.helpers;
  window.MagicFrame.register("pegelstand", {
    render(el, ctx) {
      if (!ctx.data) { el.innerHTML = '<div class="xsmall dimmed">…</div>'; return true; }
      el.innerHTML = `<div class="medium bright">${ctx.h.number(ctx.data.cm)} cm</div>`;
      // return false to hide the module, e.g. when there is nothing to show
    },
    tick(el, ctx) { /* optional: runs every second */ },
  });
})();
```

`render` runs when the settings or the data change. `ctx` has:

| | |
|---|---|
| `config` | the module's settings (secrets are empty, `has_<key>` says whether one is set) |
| `data` | what `fetch.py` returned last (or `null`) |
| `error` | a readable error text if the last fetch failed |
| `at` | when the data was fetched (epoch seconds) |
| `lang` | `de`, `en` or `es` |
| `region`, `place`, `clock24` | where the module is, the location name, 24-hour clock |
| `h` | helpers: `esc`, `t({de,en,es}, values)`, `time(epoch)`, `dayName(epoch)`, `number(v, digits)`, `degrees(v, imperial)`, `icon(name)`, `weatherIcon(wmoCode, isDay)`, `weatherText(wmoCode)`, `nowSec()` |

CSS classes from MagicMirror work as you'd expect: `xsmall small medium large xlarge`, `bright normal dimmed`, `light thin`. Text alignment follows the region (left, right, centre). Scope your own CSS with `.m-<type>`.

## fetch.py

```python
def fetch(config, ctx):
    row = ctx["get"]("https://example.org/api", params={"q": config["station"]})
    return {"cm": row["value"]}
```

Magic Frame imports this file in its own Python process and calls `fetch(config, ctx)` on the `every` schedule. Return anything JSON-serialisable; it becomes `ctx.data` in the scene. `ctx` has `lat`, `lon`, `lang`, `imperial`, `get(url, params=None, headers=None, expect="json"|"text")` (with Magic Frame's User-Agent and timeouts), `SourceError(code, detail)` and `log(text)`. Raise `ctx["SourceError"]("unreachable")`, `("key")`, `("format")`, `("http:503")` etc. for readable errors on the page.

Use only the Python standard library and `requests` (and `icalendar`, which Magic Frame already has): your plugin's own requirements may live in a different environment.

## Trust

Add-on modules run with the same rights as Magic Frame. Only install modules you trust.
