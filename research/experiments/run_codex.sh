#!/usr/bin/env bash
# Run every prompt in prompts.json against an OpenAI model via the Codex CLI (subscription auth),
# in an empty read-only sandbox with web search disabled, so we measure model priors only.
# Usage: ./run_codex.sh <model> [<model> ...]      e.g. ./run_codex.sh gpt-5.6-sol
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/results"
WORKDIR="/private/tmp/claude-502/-Users-jatorre-workspace-openvis-summit-2026/0fcc559d-5a16-4e20-8d22-d6dafbba654f/scratchpad/codex-cwd"
mkdir -p "$OUT" "$WORKDIR"
MODELS=("$@"); [ ${#MODELS[@]} -eq 0 ] && { echo "usage: $0 <model> ..."; exit 1; }
CONCURRENCY=4

run_one() {
  local model="$1" key="$2"
  local prompt; prompt="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prompts"][sys.argv[2]])' "$HERE/prompts.json" "$key")"
  local slug="codex-$model"; local dir="$OUT/$slug"; mkdir -p "$dir"
  local f="$dir/$key.md"
  [ -s "$f" ] && { echo "skip $slug/$key (exists)"; return; }
  local start; start=$(date +%s)
  ( cd "$WORKDIR" && timeout 600 codex exec -m "$model" --skip-git-repo-check --ephemeral -s read-only -C "$WORKDIR" \
      -c 'web_search="disabled"' -o "$f.tmp" "$prompt" ) > "$f.log" 2>&1
  local rc=$?
  local secs=$(( $(date +%s) - start ))
  if [ $rc -eq 0 ] && [ -s "$f.tmp" ]; then
    { echo "<!-- model: $model | prompt: $key | seconds: $secs | backend: codex-cli sandbox=read-only web_search=disabled -->"; cat "$f.tmp"; } > "$f"
    rm -f "$f.tmp" "$f.log"; echo "ok   $slug/$key (${secs}s)"
  else
    echo "FAIL $slug/$key rc=$rc (${secs}s): $(tail -c 300 "$f.log" | tr '\n' ' ')"; rm -f "$f.tmp"
  fi
}
export -f run_one; export HERE OUT WORKDIR

KEYS="$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["prompts"].keys()))' "$HERE/prompts.json")"
for m in "${MODELS[@]}"; do for k in $KEYS; do echo "$m $k"; done; done \
  | xargs -P "$CONCURRENCY" -n 2 bash -c 'run_one "$0" "$1"'
echo "DONE $(date)"
