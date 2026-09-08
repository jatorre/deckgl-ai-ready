# Making deck.gl AI-Ready

Talk, research and experiments for **"Making deck.gl AI-Ready: Declarative Specs as an Agent-Native Interface for Maps"**, Open Visualization Collaborator Summit, ETH Zürich, 9 September 2026. Speaker: Javier de la Torre (CARTO).

- **Slides:** https://jatorre.github.io/deckgl-ai-ready/ (reveal.js, press `S` for speaker notes)
- **Outline with speaker notes:** [`talk/OUTLINE.md`](talk/OUTLINE.md)

## What is in here

| Path | What |
|---|---|
| `research/experiments/RESULTS.md` | Experiment 1: what 10 models recommend for maps, how current their deck.gl knowledge is, whether the MapLibre relationship confuses them, and whether they can write `@deck.gl/json`. Raw answers in `results/`. |
| `research/experiments/mapbench/` | Experiment 2: 7 frontier models (Opus 4.8, Fable 5.1, GPT-5.6 Sol, GPT-6 Astra, Gemini 3.1 Pro, Gemini 3.8 Flash, GLM 5.3) build 4 specified single-page deck.gl maps plus one open brief; rendered headlessly, scored with a fixed rubric. `report.html` is the visual grid, `RESULTS.md` the write-up, `out/` the generated maps. |
| `talk/` | Outline with speaker notes, the live deck.gl title map (`title-map.html`), brand assets, and `build-grids.py`, which feeds the slides' result grids from the experiment data. |
| `research/experiments/*.sh`, `*.py`, `*.mjs` | The harnesses. Model calls go through the `claude` CLI, the Codex CLI, a LiteLLM proxy and OpenRouter; keys are read from an untracked `.env`. |

Everything was researched, run and written with Claude Code in the two days before the talk; the session is linked from the commits.

## Proposal pull requests

The suggestions in the talk were opened as draft PRs against `visgl/deck.gl` the day before the talk, each disclosing AI assistance: [#10677 llms.txt](https://github.com/visgl/deck.gl/pull/10677), [#10678 agent skill and AI guide](https://github.com/visgl/deck.gl/pull/10678), [#10679 JSON v2 RFC](https://github.com/visgl/deck.gl/pull/10679).

## License

Code and harnesses: MIT. Slides and text: CC BY 4.0. Model outputs in `results/` and `mapbench/out/` are reproduced as generated for research purposes.
