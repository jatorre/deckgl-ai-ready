#!/usr/bin/env bash
# Run every prompt in prompts.json against a set of Claude models via the claude CLI,
# with tools disabled and no user/project settings, so we measure model priors only.
# Usage: ./run_claude.sh [model ...]
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/results"
WORKDIR="/private/tmp/claude-502/-Users-jatorre-workspace-openvis-summit-2026/0fcc559d-5a16-4e20-8d22-d6dafbba654f/scratchpad/exp-cwd"
mkdir -p "$OUT" "$WORKDIR"
MODELS=("$@")
[ ${#MODELS[@]} -eq 0 ] && MODELS=(claude-haiku-4-5-20251001 claude-sonnet-5 claude-opus-5)
CONCURRENCY=6

run_one() {
  local model="$1" key="$2"
  local prompt; prompt="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prompts"][sys.argv[2]])' "$HERE/prompts.json" "$key")"
  local dir="$OUT/$model"; mkdir -p "$dir"
  local f="$dir/$key.md"
  [ -s "$f" ] && { echo "skip $model/$key (exists)"; return; }
  local start; start=$(date +%s)
  ( cd "$WORKDIR" && timeout 420 claude -p "$prompt" --model "$model" --tools "" \
      --no-session-persistence --setting-sources "" --output-format text < /dev/null ) > "$f.tmp" 2> "$f.err"
  local rc=$?
  local secs=$(( $(date +%s) - start ))
  if [ $rc -eq 0 ] && [ -s "$f.tmp" ]; then
    { echo "<!-- model: $model | prompt: $key | seconds: $secs | backend: claude-cli tools=none -->"; cat "$f.tmp"; } > "$f"
    rm -f "$f.tmp" "$f.err"; echo "ok   $model/$key (${secs}s)"
  else
    echo "FAIL $model/$key rc=$rc (${secs}s): $(head -c 200 "$f.err")"; rm -f "$f.tmp"
  fi
}
export -f run_one; export HERE OUT WORKDIR

KEYS="$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["prompts"].keys()))' "$HERE/prompts.json")"
for m in "${MODELS[@]}"; do for k in $KEYS; do echo "$m $k"; done; done \
  | xargs -P "$CONCURRENCY" -n 2 bash -c 'run_one "$0" "$1"'
echo "DONE $(date)"
