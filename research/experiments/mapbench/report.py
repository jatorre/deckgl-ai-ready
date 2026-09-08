#!/usr/bin/env python3
"""Build report.html: a task x model grid of screenshots with judge scores and render flags. Self-contained (thumbnails inlined)."""
import base64, json, os, subprocess, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "tasks.json")))
slugs = list(cfg["models"]); tasks = list(cfg["tasks"])

def thumb_b64(png, width=560):
    if not png or not os.path.exists(png): return None
    tp = png.replace(".png", f".w{width}.jpg")
    if not os.path.exists(tp):
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "70", "-Z", str(width), png, "--out", tp], capture_output=True)
    return "data:image/jpeg;base64," + base64.b64encode(open(tp, "rb").read()).decode()

def load(p):
    return json.load(open(p)) if os.path.exists(p) else None

cells = {}
for s in slugs:
    for t in tasks:
        rep = load(os.path.join(HERE, "render", s, f"{t}.json")); jd = load(os.path.join(HERE, "judge", s, f"{t}.json")); meta = load(os.path.join(HERE, "out", s, f"{t}.meta.json"))
        cells[(s, t)] = {"rep": rep, "judge": jd, "meta": meta}

def score_cell(c):
    j = c["judge"]; r = c["rep"]
    if not j: return "<div class='sc none'>not judged</div>"
    bars = "".join(f"<span title='{k}'>{k[:4]} {j.get(k,0)}</span>" for k in ["renders", "spec_compliance", "cartography", "interactivity", "api_currency"])
    flags = []
    if r:
        if r.get("fatal"): flags.append("fatal")
        if r.get("page_errors"): flags.append(f"{len(r['page_errors'])} js err")
        if r.get("http_errors"): flags.append(f"{len(r['http_errors'])} http 4xx")
        rf = [x for x in r.get("request_failed", []) if "mapbox-gl.css" not in x]  # v8 dist bundle auto-injects a mapbox css link; blocked, harmless
        if rf: flags.append(f"{len(rf)} req failed")
        if len(rf) != len(r.get("request_failed", [])): flags.append("v8 bundle css probe")
    notes = "".join(f"<li>{H.escape(n)}</li>" for n in j.get("notes", [])[:3])
    return (f"<div class='sc'><b>{j['total']}/17</b> <span class='v'>deck.gl {H.escape(str(j.get('deckgl_version')))} · {H.escape(str(j.get('basemap_integration')))}</span>"
            f"<div class='bars'>{bars}</div><div class='flags'>{' · '.join(flags) or 'clean render'}</div><ul>{notes}</ul></div>")

totals = {s: sum((cells[(s, t)]["judge"] or {}).get("total", 0) for t in tasks) for s in slugs}
judged = {s: sum(1 for t in tasks if cells[(s, t)]["judge"]) for s in slugs}
rows = []
for t in tasks:
    tds = []
    for s in slugs:
        c = cells[(s, t)]; shot = c["rep"]["screenshots"].get("t8") if c["rep"] and c["rep"].get("screenshots") else None
        b64 = thumb_b64(os.path.join(HERE, shot)) if shot else None
        img = f"<a href='out/{s}/{t}.html' target='_blank'><img src='{b64}' loading='lazy'></a>" if b64 else "<div class='noimg'>no screenshot</div>"
        secs = c["meta"]["seconds"] if c["meta"] else "?"
        tds.append(f"<td>{img}{score_cell(c)}<div class='meta'>{secs}s gen · <a href='out/{s}/{t}.html' target='_blank'>open</a> · <a href='render/{s}/{t}.t14.png' target='_blank'>t14</a></div></td>")
    rows.append(f"<tr><th class='task'><div>{H.escape(cfg['tasks'][t]['title'])}</div><small>{H.escape(cfg['tasks'][t]['probe'])}</small></th>{''.join(tds)}</tr>")
head = "".join(f"<th><div class='m'>{H.escape(s)}</div><div class='tot'>{totals[s]}/{17*len(tasks)}<small> ({judged[s]}/{len(tasks)} judged)</small></div></th>" for s in slugs)
page = f"""<!doctype html><html><head><meta charset='utf-8'><title>deck.gl single-page map generation, frontier models, Sept 2026</title>
<style>body{{font:14px system-ui,sans-serif;margin:16px;color:#222;background:#fafafa}} h1{{font-size:20px;margin:0 0 4px}} p.sub{{margin:0 0 14px;color:#555;max-width:1100px}}
table{{border-collapse:collapse}} th,td{{border:1px solid #ddd;vertical-align:top;padding:6px;background:#fff}} th.task{{width:170px;text-align:left;font-weight:600}} th.task small{{display:block;color:#777;font-weight:400;margin-top:4px}}
th .m{{font-weight:700}} th .tot{{font-weight:400;color:#444}} img{{width:280px;height:175px;object-fit:cover;display:block;border:1px solid #ccc}} .noimg{{width:280px;height:175px;background:#eee;color:#999;display:flex;align-items:center;justify-content:center}}
.sc{{margin-top:6px;font-size:12px}} .sc.none{{color:#999}} .bars span{{display:inline-block;background:#eef;border-radius:3px;padding:1px 5px;margin:2px 3px 0 0}} .flags{{color:#a33;margin-top:3px}} .v{{color:#666}} ul{{margin:4px 0 0 14px;padding:0;color:#444}} li{{margin:2px 0}} .meta{{font-size:11px;color:#888;margin-top:4px}}
</style></head><body><h1>How well do frontier models build single-page deck.gl maps?</h1>
<p class='sub'>One shot, no tools, identical prompt per task, run {os.popen('date +%Y-%m-%d').read().strip()} via OpenRouter. Rendered headlessly at 1280×800; thumbnail is the 8-second screenshot. Scores are a fixed 17-point rubric applied by Claude Fable 5.1 as judge (renders 0–2, spec compliance 0–5, cartography 0–5, interactivity 0–3, API currency 0–2) over the code, the render report and three screenshots. Click a thumbnail to open the live map.</p>
<table><tr><th class='task'>Task</th>{head}</tr>{''.join(rows)}</table></body></html>"""
open(os.path.join(HERE, "report.html"), "w").write(page)
print("report.html written;", sum(1 for c in cells.values() if c["judge"]), "judged cells of", len(cells))
