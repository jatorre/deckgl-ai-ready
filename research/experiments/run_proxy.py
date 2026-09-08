#!/usr/bin/env python3
"""Run every prompt in prompts.json against OpenAI-compatible models behind the LiteLLM proxy.

Credentials are read from ~/workspace/simpleAgentMap/.env.local (LITELLM_BASE_URL, LITELLM_API_KEY)
and never printed. Results land in results/<model-slug>/<prompt>.md next to the Claude CLI runs.

Usage: ./run_proxy.py <model-id> [<model-id> ...]
"""
import concurrent.futures as cf
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
ENV = os.path.expanduser("~/workspace/simpleAgentMap/.env.local")


def load_env(path):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def slug(model):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model.split("::")[-1])


def call(base, key, model, prompt, timeout=420):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"], d.get("usage", {})


def run_one(base, key, model, pkey, prompt):
    d = os.path.join(OUT, slug(model))
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"{pkey}.md")
    if os.path.exists(f) and os.path.getsize(f) > 0:
        return f"skip {slug(model)}/{pkey}"
    t0 = time.time()
    try:
        text, usage = call(base, key, model, prompt)
    except Exception as e:  # noqa: BLE001
        return f"FAIL {slug(model)}/{pkey}: {str(e)[:160]}"
    secs = int(time.time() - t0)
    with open(f, "w") as fh:
        fh.write(f"<!-- model: {model} | prompt: {pkey} | seconds: {secs} | backend: litellm-proxy | usage: {json.dumps(usage)} -->\n")
        fh.write(text or "")
    return f"ok   {slug(model)}/{pkey} ({secs}s)"


def main():
    models = sys.argv[1:]
    if not models:
        print(__doc__)
        sys.exit(1)
    env = load_env(ENV)
    base, key = env["LITELLM_BASE_URL"], env["LITELLM_API_KEY"]
    prompts = json.load(open(os.path.join(HERE, "prompts.json")))["prompts"]
    jobs = [(m, k, p) for m in models for k, p in prompts.items()]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for msg in ex.map(lambda j: run_one(base, key, *j), jobs):
            print(msg, flush=True)
    print("DONE", time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
