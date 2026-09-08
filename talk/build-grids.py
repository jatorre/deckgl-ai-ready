#!/usr/bin/env python3
"""Write talk/grid-data.js from the mapbench judge results so the slides' Q2 grids stay in sync with the data."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); MB = os.path.join(HERE, "..", "research", "experiments", "mapbench")
cfg = json.load(open(os.path.join(MB, "tasks.json")))
T4 = ["T1_airports_points", "T2_vancouver_choropleth", "T3_uk_accidents_hexagons", "T4_trips_animation"]

def load(p):
    return json.load(open(p)) if os.path.exists(p) else None

scores, caps = {}, {}
for slug in cfg["models"]:
    js = {t: load(os.path.join(MB, "judge", slug, f"{t}.json")) for t in T4 + ["T5_showcase"]}
    if any(js[t] for t in T4):
        scores.setdefault(slug, {})["total4"] = sum((js[t] or {}).get("total", 0) for t in T4)
    if js["T5_showcase"]:
        scores.setdefault(slug, {})["T5"] = js["T5_showcase"]["total"]
        notes = js["T5_showcase"].get("notes") or []
        cap = notes[0] if notes else ""
        cap = re.sub(r"\s+", " ", cap).strip()
        if len(cap) > 118: cap = cap[:115].rsplit(" ", 1)[0] + "…"
        caps[slug] = cap.replace("\\", "").replace("`", "")

note = "Same data, no requirements beyond the brief. Caption is the judge's first note; same 17-point rubric. Click a thumbnail for the live page."
out = "window.__SCORES__ = %s;\nwindow.__CAPS__ = %s;\nwindow.__SHOWCASE_NOTE__ = %s;\n" % (
    json.dumps(scores, indent=1), json.dumps(caps, indent=1, ensure_ascii=False), json.dumps(note))
open(os.path.join(HERE, "grid-data.js"), "w").write(out)
print("grid-data.js:", {k: v for k, v in scores.items()})
