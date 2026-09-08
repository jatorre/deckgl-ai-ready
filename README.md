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

The suggestions in the talk were turned into proposals the day before the talk, each disclosing AI assistance and revised after an independent review pass: draft PRs [#10677 llms.txt](https://github.com/visgl/deck.gl/pull/10677) and [#10678 agent skill and AI guide](https://github.com/visgl/deck.gl/pull/10678) against `visgl/deck.gl`, the AI-assisted contributions policy for the vis.gl developer process ([visgl/tsc #20](https://github.com/visgl/tsc/pull/20)) with its deck.gl companion ([#10680](https://github.com/visgl/deck.gl/pull/10680)), and the `@deck.gl/json` v2 proposal [posted on the v2 tracker](https://github.com/visgl/deck.gl-community/issues/596#issuecomment-5583845859) with the [full draft RFC](https://github.com/jatorre/deck.gl/blob/json-v2-rfc/dev-docs/RFCs/proposals/json-v2-agent-interface-rfc.md) kept on the fork (the deck.gl PR for it, #10679, was closed in favour of the tracker where v2 incubates).

## License

Code and harnesses: MIT. Slides and text: CC BY 4.0. Model outputs in `results/` and `mapbench/out/` are reproduced as generated for research purposes.
