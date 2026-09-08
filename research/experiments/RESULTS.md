# What do models recommend for maps, and how well do they know deck.gl?

Experiment run 2026-09-07/08 for the Zurich talk. 8 prompts × 10 models, one sample each, no tools, no retrieval. Raw answers in `results/<model>/<prompt>.md`, prompts in `prompts.json`, automated signals in `scores.json`, hand grading below. Section 6 covers the two frontier models (Claude Fable 5.1, GPT-5.6-sol) that were the original target; sections 1 to 4 tabulate the eight earlier models and section 6 reports how the frontier pair moves each count.

**Models.** Claude Haiku 4.5, Sonnet 5, Opus 5 and **Fable 5.1** via the `claude` CLI with `--tools ""` and no project settings (so the answers reflect a coding agent's priors, not the docs). **GPT-5.6-sol** via the Codex CLI (`codex exec`, empty read-only sandbox, `web_search="disabled"`, subscription auth; unknown model ids are rejected with a 400, so the id is honored). GPT-4o, GPT-5-mini, GPT-5.2, Gemini 3.7 Flash, Gemini 3.1 Pro via CARTO's LiteLLM proxy as plain chat completions. Reasoning models needed a larger budget on three prompts and were rerun; the rerun is what is graded.

**Ground truth used for grading.** deck.gl latest is 9.4.0 (npm, released 2026-09-05); 9.3.0 shipped 2026-04-13. `@deck.gl/mapbox` `MapboxOverlay` is added with `map.addControl()`. 9.4 introduced `@deck.gl/maplibre` (first beta 2026-08-28) exporting `MapLibreOverlay`, "the recommended deck.gl integration for MapLibre". `leaflet-h3` does not exist on npm.

## 1. Which library do models pick? (P1, P2, P3, P4, P8)

| Prompt | Leaflet | MapLibre | Mapbox | deck.gl | Other |
|---|---|---|---|---|---|
| P1 · 2M GPS points, colored by speed | 0 | 2 (GPT-5.2, GPT-5-mini) | 1 (GPT-4o, deck.gl co-mentioned) | 5 (Haiku, Sonnet, Opus, both Geminis) | |
| P2 · simple airports GeoJSON + tooltip | 7 | 1 (Opus) | 0 | 0 | |
| P3 · H3 hexagons colored by count | 1 (GPT-4o, with a non-existent `leaflet-h3` plugin) | 1 (Haiku + h3-js) | 0 | 5 (Sonnet, Opus, GPT-5-mini, both Geminis) | 1 (GPT-5.2 answered in Python/folium) |
| P4 · best OSS map library for React in 2026 | 0 | 6 | 2 (Haiku, GPT-4o) | 0 as primary; Opus names it runner-up | |
| P8 · single HTML file with 5 city markers | 8 | 0 | 0 | 0 | |

Reading: deck.gl lives in model priors as the answer to "millions of points" or "H3", never as the default map library. Leaflet owns anything simple; MapLibre owns the React default. Two OpenAI models solved the 2M-point case without deck.gl at all (GPT-5.2: tippecanoe + vector tiles + a MapLibre circle layer). That is the competitive signal: for its flagship use case deck.gl is one of two answers, not the answer.

Side observation for CARTO: in P7, 7 of 8 models chose `basemaps.cartocdn.com` Positron as "a light basemap" without being told about CARTO. CARTO basemaps are the de-facto default basemap in model priors.

## 2. Do models know current deck.gl? (P6)

| Model | Version it targets | Era | Notes |
|---|---|---|---|
| Haiku 4.5 | 8.12.0 | v8 | |
| GPT-4o | 8.11.0 | v8 | says "as of October 2023" |
| GPT-5-mini | 8.10.8 | v8 | says "as of 2024-06" |
| GPT-5.2 | 9.0.0 | v9 | |
| Gemini 3.1 Pro | 9.0.0 | v9 | |
| Sonnet 5 | 9.1.0 | v9 | pairs CARTO style with `mapbox-gl@3.9` and `react-map-gl/mapbox`, which needs a Mapbox token |
| Gemini 3.7 Flash | 9.1.4 | v9 | |
| Opus 5 | 9.1.x | v9 | adds "confirm with `npm view deck.gl version` before pinning" |

Three of eight write v8 code. Zero of eight know 9.2 (May 2025), 9.3 or 9.4. Without docs access, a coding agent ships deck.gl that is one to two years behind, and the v8 to v9 change was the breaking one.

## 3. Is the MapLibre relationship confusing? (P5)

| Model | Package | Class | Attach | Verdict |
|---|---|---|---|---|
| Sonnet 5, Opus 5, GPT-5.2, Gemini 3.7, Gemini 3.1 | `@deck.gl/mapbox` | `MapboxOverlay` | `addControl` | correct for ≤9.3 |
| Haiku 4.5 | `@deck.gl/mapbox` | `MapboxOverlay` | `map.addLayer(overlay)` | wrong attach call |
| GPT-4o, GPT-5-mini | `@deck.gl/maplibre` | `MaplibreLayer` | `map.addLayer` | package now exists (since 2026-09-05) but class and API don't |

Every one of the five correct answers stopped to explain that a module named mapbox works with MapLibre "despite the name" or "because MapLibre is a fork". The two weaker GPT models guessed the package name developers expected. Two days before this experiment deck.gl 9.4 shipped exactly that package. The confusion was real enough that the project renamed the module, and now the training data for every model says the old name. Only docs an agent can read at run time will overwrite that.

## 4. Can models write `@deck.gl/json`? (P7: choropleth of countries by population)

| Model | `@@type` | `views` block | Data-driven fill color | Verdict |
|---|---|---|---|---|
| Opus 5 | yes | yes | `@@=` ternary chain over `properties.population` | valid |
| Gemini 3.7 Flash | yes | yes | `@@=` ternary | valid |
| Gemini 3.1 Pro | yes | yes | `@@=` ternary | valid |
| Sonnet 5 | yes | yes | `{"@@function": "colorContinuous", "attr", "colors": "Sunset"}` | valid only if `@deck.gl/carto` helpers are registered; dropped by stock converter |
| Haiku 4.5 | yes | no | invented `{"@@type": "colorBinScale", accessor, domain, range}` inside a `version/config` wrapper | invalid |
| GPT-4o | yes | no | Mapbox style expression `["get", "population", ...]` | invalid |
| GPT-5.2 | yes | yes | invented `{"@@type": "Expression", "expression": ["interpolate", ...]}` | invalid |
| GPT-5-mini | no, uses `"type"` | plain | `mapbox://` style + `["interpolate", ["linear"], ["get", "population"], ...]` | invalid |

Reading: the `@@type` syntax is mostly known (7 of 8). The failure is semantic, in data-driven styling. Four of eight reached for the Mapbox/MapLibre style-spec expression grammar, because that is the declarative map styling language the training data is full of. One model reached for CARTO's helper vocabulary. Nobody produced anything the stock converter would reject loudly; every invalid accessor would be silently dropped or become a constant.

Three vocabularies exist today for the same idea, a color scale over an attribute: CARTO's `colorBins / colorContinuous / colorCategories`, SQLRooms' `colorScale {type, scheme}`, and hand-written `@@=` ternaries. Models default to a fourth, Mapbox expressions.

## 5. Implications for the talk

1. **Positioning.** deck.gl is a "when the data is big" library in every model's head. Whether that is fine or a problem is a question for the room, but it means deck.gl will be chosen by agents only if the prompt already knows it needs it.
2. **Docs for agents are not optional.** Version drift and the MapLibre rename are both facts models cannot know. MapLibre ships llms.txt and agent skills; Mapbox ships MCP servers; luma.gl ships llms.txt; deck.gl ships none. This experiment is the quantitative slide for that ask.
3. **For `@deck.gl/json` v2:** a schema catches every invalid P7 above. Beyond that, two provocations. Consider accepting Mapbox-style expression arrays as an accessor syntax, since models and humans already speak it. And standardize one scale-helper vocabulary in core rather than three vendor ones.
4. **Silent failure again.** Not one of the five invalid specs would produce an error today. This matches what CARTO and SQLRooms both had to build around.

## 6. Frontier models: Claude Fable 5.1 and GPT-5.6-sol

| Prompt | Fable 5.1 | GPT-5.6-sol |
|---|---|---|
| P1 · 2M points | deck.gl on MapLibre, binary attributes, `MapboxOverlay`, CARTO Positron | deck.gl on MapLibre, binary attributes, `MapboxOverlay` via esm.sh |
| P2 · simple GeoJSON | **MapLibre** ("Leaflet is simpler for tiny datasets, but world airports are around 7,000 points") | **MapLibre** |
| P3 · H3 | deck.gl `H3HexagonLayer` + MapLibre + d3-scale | deck.gl `H3HexagonLayer` + `react-map-gl/maplibre` |
| P4 · React 2026 | MapLibre via react-map-gl; runner-up Leaflet; "composes cleanly with deck.gl" | MapLibre via `react-map-gl/maplibre`; runner-up Leaflet |
| P5 · deck.gl on MapLibre | `@deck.gl/mapbox` `MapboxOverlay` + `addControl`, correct for ≤9.3, good interleaved/`beforeId` notes | **`@deck.gl/maplibre` `MapLibreOverlay` + `addControl`**, links the official "using with MapLibre" guide. This is the deck.gl 9.4 API, three days old at test time. Only model to produce it |
| P6 · version | 9.1, hedged ("a later 9.x minor may exist"); adds `@luma.gl/core` and `@luma.gl/webgl` to the install, which is unnecessary | 9.1.14; no hedge |
| P7 · `@deck.gl/json` | valid: `@@type`, `views`, `@@=` ternary over `properties.population` | `@@function: colorContinuous` with `attr: "properties.population"`, CARTO's helper vocabulary; dropped by the stock converter, and the `properties.` prefix is wrong even for CARTO's helper |
| P8 · single HTML | Leaflet | Leaflet 1.9.4 with SRI hashes |

How the frontier pair changes the picture:

- **Library picks.** Same shape as the field, one shift: both frontier models pick MapLibre, not Leaflet, for the simple GeoJSON map. Leaflet is becoming the single-file-page answer only. deck.gl is still chosen only when the prompt signals scale or H3. With all ten models: 2M points → deck.gl 7 of 10; H3 → deck.gl 7 of 10; simple GeoJSON → Leaflet 7 of 10, MapLibre 3 of 10; React default → MapLibre 8 of 10; single file → Leaflet 10 of 10.
- **Version drift does not go away at the frontier.** Both target 9.1. Across ten models: 3 write v8, 7 write 9.0 or 9.1, none know 9.2, 9.3 or 9.4. Fable hedges explicitly; Opus told the user to check npm. Those hedges are the best behaviour available without docs access.
- **MapLibre.** GPT-5.6-sol knows the 9.4 module. Fable gives the pre-9.4 correct answer. So the two most capable models now disagree on the package to install, and both are right depending on the deck.gl version the user has. With ten models: 6 correct pre-9.4 answers, 1 correct 9.4 answer, 1 wrong attach call, 2 invented class names on the right package name.
- **`@deck.gl/json`.** Fable is valid. GPT-5.6-sol joins Sonnet 5 in emitting CARTO's `colorContinuous` helper into a stock deck.gl spec. With ten models: 4 valid accessors, 2 CARTO-vocabulary accessors, 4 Mapbox-expression or invented accessors. CARTO's docs are the strongest single influence on how models write deck.gl JSON styling.
- **Basemaps.** Fable used CARTO Positron or Dark Matter in P1, P3, P5, P7 unprompted; GPT-5.6-sol used Positron in P5 and P7. Ten-model count for the P7 "light basemap": 9 CARTO Positron, 1 `mapbox://`.

## Caveats

Single sample per cell, default temperature, three backends with different system prompts. Treat counts as directional. Rerun with `./run_claude.sh` and `./run_proxy.py <model-id>`; delete a result file to regenerate it.
