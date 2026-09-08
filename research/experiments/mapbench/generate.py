#!/usr/bin/env python3
"""Generate single-page deck.gl maps with frontier models via OpenRouter. Usage: ./generate.py [model-slug ...]"""
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(HERE, "..", ".env")
key = [l.split("=",1)[1].strip().strip('"') for l in open(ENV) if l.startswith("OPENROUTER_API_KEY=")][0]
cfg = json.load(open(os.path.join(HERE, "tasks.json")))
OUT = os.path.join(HERE, "out")

def extract_html(text):
    blocks = re.findall(r"```(?:html|HTML)?\s*\n(.*?)```", text, re.S)
    cands = [b for b in blocks if "<html" in b.lower() or "<!doctype" in b.lower()] or blocks
    if cands:
        return max(cands, key=len).strip()
    m = re.search(r"(<!DOCTYPE html.*?</html>|<html.*?</html>)", text, re.S | re.I)
    return m.group(1) if m else text.strip()

def run(slug, model, tkey, task):
    d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
    html_path, meta_path = os.path.join(d, f"{tkey}.html"), os.path.join(d, f"{tkey}.meta.json")
    if os.path.exists(meta_path): return f"skip {slug}/{tkey}"
    prompt = cfg["preamble"] + "\n\n" + task["prompt"]
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 24000}
    if "gpt-6" in model:  # reasoning counts toward the budget on OpenAI models
        body["max_tokens"] = 40000
    if "glm" in model:  # GLM 5.3 spends the whole budget on hidden reasoning by default (24k reasoning tokens, empty content)
        body["reasoning"] = {"max_tokens": 8000}; body["max_tokens"] = 32000  # thinking is mandatory on this endpoint; effort=low still burned 40k reasoning tokens on 3 of 4 tasks
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "HTTP-Referer": "https://carto.com", "X-Title": "deckgl-mapbench"})
    t0 = time.time()
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=(600 if "glm" in model else 900)))
    except urllib.error.HTTPError as e:
        return f"FAIL {slug}/{tkey} HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e:
        return f"FAIL {slug}/{tkey}: {str(e)[:200]}"
    secs = round(time.time() - t0, 1)
    msg = resp["choices"][0]["message"]
    text = msg.get("content") or ""
    html = extract_html(text)
    open(html_path, "w").write(html)
    open(os.path.join(d, f"{tkey}.raw.md"), "w").write(text)
    meta = {"slug": slug, "model": model, "task": tkey, "seconds": secs, "finish_reason": resp["choices"][0].get("finish_reason"),
            "usage": resp.get("usage", {}), "html_bytes": len(html), "raw_chars": len(text),
            "looks_like_html": html.lower().lstrip().startswith(("<!doctype", "<html"))}
    json.dump(meta, open(meta_path, "w"), indent=1)
    return f"ok   {slug}/{tkey} {secs}s html={len(html)}b finish={meta['finish_reason']} out_tokens={meta['usage'].get('completion_tokens')}"

if __name__ == "__main__":
    slugs = sys.argv[1:] or list(cfg["models"])
    jobs = [(s, cfg["models"][s], k, t) for s in slugs for k, t in cfg["tasks"].items()]
    with cf.ThreadPoolExecutor(10) as ex:
        for r in ex.map(lambda j: run(*j), jobs): print(r, flush=True)
    print("DONE", time.strftime("%H:%M:%S"))
