# Making deck.gl AI-Ready — talk outline

Open Visualization Collaborator Summit, ETH Zürich, Wed 9 Sept 2026, 11:45–12:10 (25 min slot: ~20 min talk, ~4 min Q&A). Speaker: Javier de la Torre, CARTO.

Structure: one opening beat, five audit questions, each with **evidence** (one slide) and **suggestions** (one slide), then three asks for Thursday's "Future of Vis.gl" discussion. Section 3 is the thesis the title promises; the other four are the audit around it.

Time plan: open 1 · Q1 3 · Q2 5 · Q3 6 · Q4 2.5 · Q5 2.5 · close 1.5 = ~21 min.

---

## 0. Title (0:00)

**Making deck.gl AI-Ready.** Declarative specs as an agent-native interface for maps. Javier de la Torre · CARTO · jatorre.github.io/deckgl-ai-ready

Notes: Everything in this talk, the experiments, the raw model outputs, the harnesses, is in that repo. Built in the last two days with a coding agent, which is itself part of the argument.

## 1. AI changed how software gets built (0:30)

Slide: one line. "Everyone in this room now builds with agents. So do deck.gl's users." Then the five questions as a list:
1. What do models recommend when someone asks for a map?
2. How well do frontier models write deck.gl?
3. How can agents drive deck.gl interactively?
4. Does our website and documentation work for AI?
5. How do we handle AI contributions?

Notes: I won't spend time on "AI is changing development". You know. What I want to do is an audit: treat agents as deck.gl's newest user group and ask, honestly, how ready we are for them. For each question I ran an experiment or read the sources, and for each I have a suggestion. Some are cheap. One is a proposal I'd like the TSC to pick up.

---

## Q1 · What do models recommend? (1:30 → 4:30)

### Slide 1a — Evidence: 10 models, 8 neutral prompts, no tools

Table (from `research/experiments/RESULTS.md`):

| Ask | Winner |
|---|---|
| 2 million GPS points colored by speed | deck.gl 7/10 (GPT-5.2 and GPT-5-mini solved it with MapLibre vector tiles) |
| Simple airports GeoJSON with tooltip | Leaflet 7/10; both newest frontier models chose MapLibre |
| H3 hexagons colored by count | deck.gl 7/10 |
| Best open-source map library for React, 2026 | MapLibre 8/10; deck.gl never primary |
| Single HTML file with five markers | Leaflet 10/10 |
| Latest deck.gl version known | 3/10 write v8; 0/10 know 9.2, 9.3 or 9.4 |
| Add deck.gl on MapLibre | 6/10 correct pre-9.4 answer, all saying "despite the name"; 1 knew the 9.4 module; 3 wrong |

Side fact: 9 of 10 picked CARTO Positron as "a light basemap" unprompted.

Notes: Claude Haiku/Sonnet/Opus/Fable through the CLI with tools off, GPT-4o/5-mini/5.2 and Gemini through a proxy, GPT-5.6-sol through Codex. One sample each, directional. The pattern is very stable though: deck.gl lives in every model's head as the answer to "millions" or "H3". Never as the default map. Leaflet is retreating to single-file pages. MapLibre is where developers, and agents, start.

### Slide 1b — What it means, what to do

- deck.gl is the "when the data is big" library in model priors. That matches its identity. Own it, and make sure the on-ramp from MapLibre is short, because that's where agents begin.
- Version drift: without docs an agent writes deck.gl one to two years old, and v8→v9 was the breaking change. Hands off to Q4.
- The MapLibre story: models needed a paragraph to explain why a module named mapbox works with MapLibre; last Friday 9.4 shipped `@deck.gl/maplibre`. The confusion was real enough to rename the module; every model's training data now says the old name.

---

## Q2 · How well do frontier models write deck.gl? (4:30 → 9:30)

### Slide 2a — The harness

Four tasks, one prompt each, one shot, no tools. Self-contained HTML, CDN only, real data from deck.gl-data, fixed viewport. Rendered headlessly in Chromium with WebGL; errors, failed requests and CDN versions captured; screenshots at 3/8/14 s. Scored on a 17-point rubric (renders 2, spec 5, cartography 5, interactivity 3, API currency 2) by Claude Fable 5.1 as judge over code + render report + screenshots. Models: Claude Fable 5.1, GPT-5.6-sol, Gemini 3.8 Flash, Gemini 3.1 Pro, GLM 5.3.

Tasks: airports as typed points with tooltip and legend; skew-aware choropleth of 4,627 Vancouver blocks with legend; extruded hexagons of 140k UK accidents with a radius slider; animated taxi trips with play/pause.

### Slide 2b — The grid (screenshots)

Embed `research/experiments/mapbench/report.html` thumbnails, or 5×4 screenshot grid. Live maps linkable.

Notes: Pause here. These are one-shot outputs. Sixteen of sixteen maps from the closed models rendered the intended data, zero page errors, zero console errors. Hover, legends, sliders, animation all wired. If you'd shown me this two years ago I would not have believed it.

### Slide 2c — Scores and the catch

| Model | Total /68 | Renders | API currency /8 | deck.gl pinned |
|---|---|---|---|---|
| GPT-5.6-sol | 61 | 4/4 | 7 | 9.1.x ×3, 8.9.36 |
| Claude Fable 5.1 | 60 | 4/4 | 6 | 9.0.x ×2, 8.9.35 ×2 |
| Gemini 3.1 Pro | 58 | 4/4 | 4 | 8.9.x ×4 (+ `window.mapboxgl = maplibregl` shim) |
| Gemini 3.8 Flash | 57 | 4/4 | 4 | 8.9.35 ×4 |
| GLM 5.3 | 32 | 1/4 | 4 | 8.9.x ×4 |

- 15 of 20 files pin a deck.gl 8.9.x bundle. Nobody used 9.2+, nobody used the 3-day-old MapLibre module.
- Only one model used the v9 overlay pattern (MapboxOverlay + addControl); the others use the v8 standalone DeckGL class.
- Hexagons and trips, the canonical showcase examples, pulled models to v8 hardest. The model copies the example's stack with its idea.
- Cartography 3–4 of 5 everywhere, no 5s: YlOrRd quantiles every time, long-tail skew unhandled, small points invisible, legends missing on trips.
- GLM 5.3: knows the vocabulary, not the contract. Shadowed the `deck` global; mutated layer props and called internal setState instead of recreating the layer; read `props.bbox` instead of `props.tile.bbox`; once pinned a version that doesn't exist. (Also: its OpenRouter endpoint spent the whole budget on mandatory reasoning until capped.)

### Slide 2d — Suggestion

The gap isn't capability. It's freshness and unwritten rules. Both are fixed by documentation an agent can read at run time, and by making the rules checkable. → Q4 and Q3.

---

## Q3 · How can agents drive deck.gl interactively? (9:30 → 15:30) — the thesis

### Slide 3a — This was designed in 2018

Quote, JSON Layers RFC, Ib Green, July 2018: "a growing need to be able to generate powerful visualizations directly from the backend… without having knowledge about how to code front-end applications." Replace *backend* with *agent*. April 2026: `@deck.gl/json` v2 tracker, goal #1 "enable LLMs to generate deck.gl visualizations". And in the module today: `console.error('Back-channel not implemented for this transport')` — the return channel was designed and never built.

Notes: So I'm not proposing a new direction. I'm asking us to finish one Ib started.

### Slide 3b — Three ways an agent holds a map (CARTO's experience)

| | State behind verbs | A document the agent writes | A picture it receives |
|---|---|---|---|
| Where | In-app map assistant | MCP tool rendering a `@deck.gl/json` spec inside the chat (MCP Apps) | CLI screenshot |
| Agent writes | one tool call per turn, ~27 verbs, ordering rules in prose | whole spec, stateless, portable | nothing; names a map |
| Agent reads | a lossy summary of the map | nothing; errors only | pixels |

Notes: We run all three in production. The verbs approach is stateful but every rule lives in prose. The document approach is portable and it is stock `@deck.gl/json` with a closed registry of CARTO layers, but it is silent on failure. Neither gives the agent eyes. Also: a stateless spec inside an MCP App means the map itself becomes an artifact that travels from chat into apps.

### Slide 3c — What it costs to make it work today

- The tool description an agent must read to write valid deck.gl JSON: ~36 KB, ~9,000 tokens. Half of it is a catalogue of *silent* failures: unregistered layer → empty map, no error; wrong layer/source pairing → empty; missing aggregation → empty; deep ternary → blank tile.
- The same service validates Vega-Lite charts with Ajv against the official 1.9 MB JSON Schema and formats errors for the model. For deck.gl specs it counts layers before and after conversion. Charts get a type system; maps get prose.
- Upstream today: unknown `@@type` → `log.warn` + `null`. Docs: "Error detection is currently limited and error messages may not be very helpful."
- Feedback design lesson: actively messaging the model about an error over an optimistic tool result made it oscillate and retry the same args. Errors-only, passive. Silence equals success. Error text is a prompt: name the legal alternatives, forbid blind retry.
- And the loop is write-only. No viewport, no feature counts, no clicks come back. The agent cannot look at its own map.

### Slide 3d — Can models write the spec? (10 models, choropleth by population)

| Outcome | Models |
|---|---|
| Valid `@@=` accessor | 4/10 (Opus, Fable, both Geminis) |
| CARTO's `colorContinuous` helper in a stock spec | 2/10 (Sonnet, GPT-5.6-sol) |
| Mapbox style-spec expressions or invented classes | 4/10 |
| Would fail loudly in today's converter | 0/10 |

`@@type` syntax: 7/10 fine. The failure is semantic: data-driven styling. Models reach for the Mapbox expression grammar, the declarative styling language the training data is full of.

### Slide 3e — Everyone is rebuilding the same thing

CARTO (closed registry, coercer, 36 KB contract) · SQLRooms (`_sqlroomsBinding`, ~60 KB of AI normalizer/validator/instructions with rules that mirror CARTO's line for line) · pydeck · kepler.gl config · noodles.gl portable JSON. Three vocabularies for "a color scale over an attribute". Meanwhile the v2 tracker's step 1, GeoJSON Zod schemas, has been an open PR since April 17.

### Slide 3f — Proposal: make `@deck.gl/json` v2 the agent interface

1. **JSON Schema from Zod**, including the compatibility rules (layer↔source, required props, expression grammar). Enables validation, structured outputs, editors.
2. **Loud failure**: a conversion report (ok / partial / error, dropped items with reasons) instead of warn-and-drop.
3. **State read-back**: viewport, layers (id, visible, count), picked object, optional screenshot. Finish the 2018 back-channel. Ship a reference MCP App.
4. **Patch semantics** for multi-turn editing (JSON Patch or deep-merge by layer id).
5. **A data-source concept** (SQL, tiles, Arrow, COG) so every vendor stops wrapping its own.
6. **Registry profiles**: core + vendor registries published with their schemas.
Two provocations: accept Mapbox-style expression arrays as an accessor syntax, since models and humans already speak it; standardize one scale-helper vocabulary in core.

Notes: deck.gl doesn't need to speak natural language. It needs to be checkable, so a model's fluency in JSON is enough. Also name the tension: the 2018 RFC's "One API" principle vs. an agent profile that is smaller and stricter. We broke One API on purpose with a closed registry. Make that a supported pattern.

---

## Q4 · Does our website and documentation work for AI? (15:30 → 18:00)

### Slide 4a — Evidence

| Site | llms.txt | Agent skills | MCP server |
|---|---|---|---|
| luma.gl (same TSC) | yes, 97 KB | | |
| maplibre.org | yes | official `maplibre-agent-skills`, 9 skills, "to inform the LLMs" | community |
| docs.mapbox.com | yes | | two official (location + DevKit for coding agents) |
| deck.gl | **404** | none | none |

Consequence measured in Q1/Q2: 15/20 generated files on v8; 0 models know 9.2+.

### Slide 4b — Suggestions

- llms.txt and page-level Markdown (luma.gl already has the pipeline).
- An official `deck.gl-agent-skills`: MapLibre integration on 9.4, v8→v9 migration, binary attributes at scale, the JSON spec, the aggregation layers' unwritten rules.
- A machine-readable what's-new.
- (If done) show the PR: "I asked an agent to make deck.gl AI-ready; here's the first PR."

---

## Q5 · How do we handle AI contributions? (18:00 → 20:30)

### Slide 5a — Evidence

- deck.gl contributing guide, PR template, TSC charter, governance and developer-process docs: zero mentions of AI or assisted contributions.
- The landscape: bans (Zig, Gentoo, QEMU, Bevy, GIMP), disclosure (curl, Linux "Assisted-by:", Apache "Generated-by:", LLVM, Kubernetes, NumPy), conditional (CPython, PyTorch). OpenJS Foundation's position after the Node.js 19k-line Claude Code PR: legal counsel says the DCO covers AI-assisted code.
- The contributions are already here: SQLRooms' deck integration was planned "with the help of gpt-5.4"; three AI-forward RFCs landed in deck.gl-community on one day; this talk's repo was built with an agent.

### Slide 5b — Suggestions

- Disclosure policy: `Assisted-by:` trailer, contributor understands and has tested the code.
- No AI on good-first-issues (LLVM's rule) to protect newcomers.
- PR template checkbox; an `AGENTS.md` so contributors' agents follow the developer process and test guidelines.
- Treat the developer-process docs as the agent's instructions: that is what they now are.

---

## Close (20:30 → 22:00)

Three asks for Thursday's Future of Vis.gl discussion:
1. Adopt `@deck.gl/json` v2 as a TSC priority with a schema and a conversion report; CARTO will bring its production evidence and help drive it.
2. Ship llms.txt and an official agent-skills repo this quarter.
3. Adopt a disclosure-based AI contribution policy.

Last line: Agents are deck.gl's newest users. They already like it. Let's make it easy for them to be right.

Repo: jatorre.github.io/deckgl-ai-ready

---

## Backup slides

- Full 10-model tables (Q1).
- Full mapbench grid with judge notes.
- The 16-item "NOT ACCEPTED" list shape (anonymized categories).
- JSON v2 tracker comments summary.
- Adjacent talks to reference: Koschinsky & Li on skill-based design (16:00 today), Elsinga on MLT (14:45), Krebs & Gervang on noodles.gl (14:15), kepler.gl and SQLRooms.
