#!/usr/bin/env python3
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); cfg = json.load(open(os.path.join(HERE, "tasks.json")))
slugs = list(cfg["models"]); tasks = list(cfg["tasks"])
print(f"{'model':18s} {'total':>7s}  " + "  ".join(f"{t[:2]:>5s}" for t in tasks) + "   renders spec carto inter api   deck.gl versions used                 basemap integration")
for s in slugs:
    js = [json.load(open(p)) if os.path.exists(p := os.path.join(HERE, "judge", s, f"{t}.json")) else None for t in tasks]
    if not any(js): print(f"{s:18s} (not judged)"); continue
    tot = sum(j["total"] for j in js if j); per = "  ".join(f"{(j['total'] if j else 0):>5d}" for j in js)
    axes = [sum(j.get(k, 0) for j in js if j) for k in ["renders", "spec_compliance", "cartography", "interactivity", "api_currency"]]
    vers = [ (json.load(open(os.path.join(HERE, "render", s, f"{t}.json"))).get("deckgl_cdn_version") or "?") for t in tasks if os.path.exists(os.path.join(HERE, "render", s, f"{t}.json"))]
    integ = sorted({j.get("basemap_integration") for j in js if j})
    print(f"{s:18s} {tot:>3d}/{17*len(tasks)}  {per}   {axes[0]:>7d} {axes[1]:>4d} {axes[2]:>5d} {axes[3]:>5d} {axes[4]:>3d}   {','.join(vers):38s} {'; '.join(map(str,integ))}")
print()
allv = [json.load(open(p)).get("deckgl_cdn_version") for p in glob.glob(os.path.join(HERE, "render", "*", "*.json"))]
v8 = sum(1 for v in allv if v and v.startswith("8")); v9 = sum(1 for v in allv if v and v.startswith("9"))
print(f"deck.gl CDN pins across {len(allv)} rendered files: v8={v8} v9={v9} other/unpinned={len(allv)-v8-v9}; distinct: {sorted(set(map(str,allv)))}")
r2 = sum(1 for p in glob.glob(os.path.join(HERE, "judge", "*", "*.json")) if json.load(open(p)).get("renders") == 2); nj = len(glob.glob(os.path.join(HERE, "judge", "*", "*.json")))
print(f"judged files with the intended data visibly rendered (renders=2): {r2}/{nj}")
