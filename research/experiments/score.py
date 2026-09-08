#!/usr/bin/env python3
import os, re, json, glob, collections
R = "results"
LIBS = {
 "leaflet": r"\bleaflet\b", "maplibre": r"maplibre", "mapbox": r"mapbox-gl|mapboxgl|Mapbox GL", "deckgl": r"deck\.gl|@deck\.gl",
 "openlayers": r"\bol\b|openlayers", "google": r"google maps|@vis\.gl/react-google-maps|maps\.googleapis", "cesium": r"cesium", "kepler": r"kepler\.gl",
}
def first_lib(text):
    # pick the library named in the first ~600 chars that isn't a negation; fall back to counts
    head = text[:700].lower()
    order = []
    for k, rx in LIBS.items():
        m = re.search(rx, head, re.I)
        if m: order.append((m.start(), k))
    return sorted(order)[0][1] if order else "?"
def signals(text):
    s = {}
    t = text
    s["libs"] = ",".join(k for k, rx in LIBS.items() if re.search(rx, t, re.I))
    s["carto"] = bool(re.search(r"\bcarto\b", t, re.I))
    v = re.findall(r"deck\.gl[^\n]{0,40}?v?(\d+\.\d+(?:\.\d+)?)|\"@deck\.gl/[a-z-]+\": *\"\^?~?(\d+\.\d+(?:\.\d+)?)|@deck\.gl/[a-z-]+@(\d+\.\d+(?:\.\d+)?)|deck\.gl@(\d+\.\d+(?:\.\d+)?)", t)
    vers = sorted({x for tup in v for x in tup if x})
    s["deck_versions"] = ",".join(vers)
    s["MapboxOverlay"] = "MapboxOverlay" in t
    s["deckgl_mapbox_pkg"] = "@deck.gl/mapbox" in t
    s["invented_maplibre_pkg"] = bool(re.search(r"@deck\.gl/maplibre", t))
    s["mapbox_token"] = bool(re.search(r"mapbox(gl)?\.accessToken|MAPBOX_TOKEN|mapboxApiAccessToken|pk\.eyJ", t))
    s["react_map_gl_maplibre"] = "react-map-gl/maplibre" in t
    s["react_map_gl_plain"] = bool(re.search(r"from ['\"]react-map-gl['\"]", t))
    s["luma_direct"] = "@luma.gl" in t
    s["at_type"] = "@@type" in t
    s["at_function"] = "@@function" in t
    s["plain_type_key"] = bool(re.search(r"\"type\"\s*:\s*\"[A-Za-z]+Layer\"", t))
    s["at_expr"] = "@@=" in t
    s["h3_layer"] = bool(re.search(r"H3HexagonLayer|H3TileLayer|h3-js", t))
    s["words"] = len(t.split())
    return s
rows = []
for f in sorted(glob.glob(f"{R}/*/*.md")):
    model, key = f.split("/")[1], os.path.basename(f)[:-3]
    t = open(f).read()
    body = re.sub(r"^<!--.*?-->\n", "", t, count=1, flags=re.S)
    s = signals(body); s["pick"] = first_lib(body)
    rows.append((key, model, s))
by_key = collections.defaultdict(list)
for key, model, s in rows: by_key[key].append((model, s))
order = ["claude-haiku-4-5-20251001","claude-sonnet-5","claude-opus-5","claude-opus-4.8","claude-fable-5-1","codex-gpt-5.6-sol","gpt-6-astra","gpt-4o","gpt-5-mini","gpt-5.2","gemini-3.7-flash","gemini-3.8-flash","gemini-3.1-pro-preview","glm-5.3"]
for key in sorted(by_key):
    print(f"\n### {key}")
    for model in order:
        for m, s in by_key[key]:
            if m != model: continue
            if key.startswith(("P1","P2","P3","P4","P8")):
                print(f"{m:28s} pick={s['pick']:10s} libs=[{s['libs']}] carto={int(s['carto'])} h3={int(s['h3_layer'])} words={s['words']}")
            elif key.startswith("P5"):
                print(f"{m:28s} MapboxOverlay={int(s['MapboxOverlay'])} @deck.gl/mapbox={int(s['deckgl_mapbox_pkg'])} @deck.gl/maplibre={int(s['invented_maplibre_pkg'])} mapboxToken={int(s['mapbox_token'])} rmg/maplibre={int(s['react_map_gl_maplibre'])} rmg-plain={int(s['react_map_gl_plain'])} vers=[{s['deck_versions']}] words={s['words']}")
            elif key.startswith("P6"):
                print(f"{m:28s} vers=[{s['deck_versions']}] luma_direct={int(s['luma_direct'])} MapboxOverlay={int(s['MapboxOverlay'])} libs=[{s['libs']}] words={s['words']}")
            elif key.startswith("P7"):
                print(f"{m:28s} @@type={int(s['at_type'])} @@function={int(s['at_function'])} @@= ={int(s['at_expr'])} plain-type-key={int(s['plain_type_key'])} words={s['words']}")
json.dump([{"prompt":k,"model":m,**s} for k,m,s in rows], open("scores.json","w"), indent=1)
