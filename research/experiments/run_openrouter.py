#!/usr/bin/env python3
"""Experiment 1 prompts against models on OpenRouter. Usage: ./run_openrouter.py <slug=openrouter/model> ...
Key read from ./.env (OPENROUTER_API_KEY), never printed. Results in results/<slug>/<prompt>.md."""
import json, os, sys, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "results")
key = [l.split("=",1)[1].strip().strip('"') for l in open(os.path.join(HERE, ".env")) if l.startswith("OPENROUTER_API_KEY=")][0]
prompts = json.load(open(os.path.join(HERE, "prompts.json")))["prompts"]
def run(slug, model, pk):
    d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True); f = os.path.join(d, f"{pk}.md")
    if os.path.exists(f) and os.path.getsize(f) > 0: return f"skip {slug}/{pk}"
    body = {"model": model, "messages": [{"role": "user", "content": prompts[pk]}], "max_tokens": 6000}
    if "glm" in model: body["reasoning"] = {"max_tokens": 4000}; body["max_tokens"] = 12000
    if "gpt-6" in model: body["reasoning"] = {"effort": "low"}; body["max_tokens"] = 16000
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "HTTP-Referer": "https://carto.com", "X-Title": "deckgl-talk-exp1"})
    t0 = time.time()
    try: d_ = json.load(urllib.request.urlopen(req, timeout=600)); txt = d_["choices"][0]["message"].get("content") or ""
    except urllib.error.HTTPError as e: return f"FAIL {slug}/{pk} HTTP {e.code}: {e.read()[:160].decode(errors='replace')}"
    except Exception as e: return f"FAIL {slug}/{pk}: {str(e)[:160]}"
    if not txt.strip(): return f"FAIL {slug}/{pk}: empty content (usage={d_.get('usage')})"
    open(f, "w").write(f"<!-- model: {model} | prompt: {pk} | seconds: {int(time.time()-t0)} | backend: openrouter | usage: {json.dumps(d_.get('usage',{}))} -->\n" + txt)
    return f"ok   {slug}/{pk} ({int(time.time()-t0)}s, {len(txt.split())} words)"
if __name__ == "__main__":
    pairs = [a.split("=",1) for a in sys.argv[1:]]
    jobs = [(s, m, pk) for s, m in pairs for pk in prompts]
    with cf.ThreadPoolExecutor(8) as ex:
        for r in ex.map(lambda j: run(*j), jobs): print(r, flush=True)
    print("DONE", time.strftime("%H:%M:%S"))
