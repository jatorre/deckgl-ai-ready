#!/usr/bin/env python3
"""LLM judge: score each rendered map against its task with a fixed rubric, using Claude Fable 5.1 via OpenRouter (vision).
Usage: ./judge.py [model-slug ...]   -> writes judge/<slug>/<task>.json"""
import base64, json, os, re, sys, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
key = [l.split("=",1)[1].strip().strip('"') for l in open(os.path.join(HERE, "..", ".env")) if l.startswith("OPENROUTER_API_KEY=")][0]
cfg = json.load(open(os.path.join(HERE, "tasks.json")))
JUDGE_MODEL = "anthropic/claude-fable-5.1"
RUBRIC = """You are grading a single-page deck.gl web map that a model generated from a task prompt. You get: the task, the generated HTML, an automated render report from headless Chromium (errors, failed requests, DOM facts), and screenshots taken 3 s, 8 s and 14 s after load at 1280x800.

Score strictly and independently on these axes. Use the screenshots as primary evidence for anything visual; use the code for anything the screenshot cannot show.
- renders (0-2): 0 = blank/broken (no map or fatal error), 1 = basemap or partial data only, 2 = the intended data visibly rendered.
- spec_compliance (0-5): every explicit requirement in the task (layer type/encoding, colors by field, sizes, tooltip, legend, controls, initial view, basemap tone, data URL used). Deduct per missing or wrong requirement.
- cartography (0-5): legibility, color choice fit for the data, contrast with basemap, visual hierarchy, legend quality, no overplotting or washed-out map. 5 = something a cartographer would ship.
- interactivity (0-3): tooltip/controls/animation implemented correctly in code and plausibly working (0 none, 3 all requested interactions wired correctly).
- api_currency (0-2): 2 = current deck.gl 9.x APIs and packages used correctly (e.g. MapboxOverlay or MapLibreOverlay added with addControl, v9 prop names), 1 = works but dated or awkward (v8 patterns, deprecated props), 0 = wrong/invented APIs.
Also extract: deckgl_version (string pinned in CDN URL or 'unpinned'), basemap_integration ('maplibre-overlay' | 'deckgl-standalone-with-mapStyle' | 'mapbox-gl' | 'none' | 'other'), and 1-3 short 'notes' naming the most important defects or strengths, quoting evidence.

Reply with ONLY a JSON object: {"renders":n,"spec_compliance":n,"cartography":n,"interactivity":n,"api_currency":n,"deckgl_version":"...","basemap_integration":"...","notes":["..."]}"""

def img(path):
    with open(path, "rb") as f: return "data:image/png;base64," + base64.b64encode(f.read()).decode()

def judge(slug, tkey):
    d = os.path.join(HERE, "judge", slug); os.makedirs(d, exist_ok=True)
    outp = os.path.join(d, f"{tkey}.json")
    if os.path.exists(outp): return f"skip {slug}/{tkey}"
    html_p = os.path.join(HERE, "out", slug, f"{tkey}.html"); rep_p = os.path.join(HERE, "render", slug, f"{tkey}.json")
    if not (os.path.exists(html_p) and os.path.exists(rep_p)): return f"missing inputs {slug}/{tkey}"
    html = open(html_p).read(); rep = json.load(open(rep_p))
    slim = {k: rep.get(k) for k in ["page_errors", "console_errors", "http_errors", "request_failed", "fatal", "deckgl_cdn_version", "maplibre_cdn_version"]}
    slim["dom"] = {k: rep.get("dom", {}).get(k) for k in ["canvases", "hasDeckGlobal", "hasMaplibreGlobal", "hasMapboxGlobal", "buttons", "sliders", "bodyText"]}
    content = [{"type": "text", "text": f"TASK:\n{cfg['preamble']}\n\n{cfg['tasks'][tkey]['prompt']}\n\nRENDER REPORT (headless Chromium):\n{json.dumps(slim)[:4000]}\n\nGENERATED HTML ({len(html)} chars):\n```html\n{html[:14000]}\n```"}]
    for t in ["t3", "t8", "t14"]:
        p = rep.get("screenshots", {}).get(t)
        if p and os.path.exists(os.path.join(HERE, p)):
            content.append({"type": "text", "text": f"Screenshot {t}:"}); content.append({"type": "image_url", "image_url": {"url": img(os.path.join(HERE, p))}})
    body = {"model": JUDGE_MODEL, "messages": [{"role": "system", "content": RUBRIC}, {"role": "user", "content": content}], "max_tokens": 3500}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "HTTP-Referer": "https://carto.com", "X-Title": "deckgl-mapbench-judge"})
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=300)); text = resp["choices"][0]["message"].get("content") or ""
    except urllib.error.HTTPError as e: return f"FAIL {slug}/{tkey} HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e: return f"FAIL {slug}/{tkey}: {str(e)[:200]}"
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    m = re.search(r"\{.*\}", text, re.S)
    try: scores = json.loads(m.group(0))
    except Exception:
        # truncated JSON: salvage the numeric fields and whatever notes closed cleanly
        try:
            nums = {k: int(v) for k, v in re.findall(r'"(renders|spec_compliance|cartography|interactivity|api_currency)"\s*:\s*(\d+)', text)}
            if len(nums) < 5: raise ValueError("incomplete")
            dv = re.search(r'"deckgl_version"\s*:\s*"([^"]*)"', text); bi = re.search(r'"basemap_integration"\s*:\s*"([^"]*)"', text)
            notes = re.findall(r'"((?:[^"\\]|\\.){20,})"', text.split('"notes"')[1]) if '"notes"' in text else []
            scores = {**nums, "deckgl_version": dv.group(1) if dv else None, "basemap_integration": bi.group(1) if bi else None, "notes": notes[:3], "salvaged": True}
        except Exception:
            return f"FAIL {slug}/{tkey} unparseable judge output: {text[:200]!r}"
    scores["total"] = sum(scores.get(k, 0) for k in ["renders", "spec_compliance", "cartography", "interactivity", "api_currency"])
    scores["judge_model"] = JUDGE_MODEL
    json.dump(scores, open(outp, "w"), indent=1)
    return f"ok   {slug}/{tkey} total={scores['total']}/17 r={scores.get('renders')} spec={scores.get('spec_compliance')} carto={scores.get('cartography')} inter={scores.get('interactivity')} api={scores.get('api_currency')} v={scores.get('deckgl_version')}"

if __name__ == "__main__":
    slugs = sys.argv[1:] or list(cfg["models"])
    jobs = [(s, k) for s in slugs for k in cfg["tasks"]]
    with cf.ThreadPoolExecutor(6) as ex:
        for r in ex.map(lambda j: judge(*j), jobs): print(r, flush=True)
