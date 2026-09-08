# How well do frontier models build single-page deck.gl maps?

Experiment run 2026-09-08 for the Zurich talk. Four tasks, one shot, no tools, identical prompt, five model configurations via OpenRouter. Each output is a self-contained HTML file rendered headlessly at 1280×800 with Playwright and Chromium (SwiftShader WebGL), then scored by Claude Fable 5.1 as judge on a fixed 17-point rubric over the code, the render report and three screenshots. Grid with thumbnails, scores and judge notes: `report.html`. Raw files: `out/<model>/<task>.html`, render reports and screenshots in `render/`, judge JSON in `judge/`. Rebuild with `./generate.py`, `node render.mjs`, `./judge.py`, `./report.py`, `./summarize.py`.

**Tasks.** T1 world airports as typed points with tooltip and legend over MapLibre. T2 choropleth of 4,627 Vancouver blocks with a skew-aware classification and an HTML legend. T3 extruded hexagon aggregation of 140k UK accident points with a radius slider, lighting and pitch. T4 animated taxi trips with play/pause and a time readout. Data from the deck.gl-data repository so loading is never the variable. Fixed initial views so screenshots are comparable.

**Rubric.** renders 0–2, spec compliance 0–5, cartography 0–5, interactivity 0–3, API currency 0–2. Max 17 per task, 68 per model.

## Scores

| Model | Total | T1 | T2 | T3 | T4 | Renders data | API currency | deck.gl pinned | Basemap integration |
|---|---|---|---|---|---|---|---|---|---|
| GPT-5.6-sol | 61/68 | 15 | 16 | 15 | 15 | 4/4 | 7/8 | 9.1.0, 9.1.5, 9.1.0, 8.9.36 | MapboxOverlay + addControl in all four |
| Claude Fable 5.1 | 60/68 | 14 | 15 | 15 | 16 | 4/4 | 6/8 | 9.0.34, 8.9.35, 8.9.35, 9.0.35 | standalone DeckGL with mapLib + mapStyle |
| Gemini 3.1 Pro | 58/68 | 14 | 15 | 14 | 15 | 4/4 | 4/8 | 8.9.33, 8.9.32, 8.9.33, 8.9.0 | standalone DeckGL, `window.mapboxgl = maplibregl` shim |
| Gemini 3.8 Flash | 57/68 | 14 | 13 | 15 | 15 | 4/4 | 4/8 | 8.9.35 ×4 | standalone DeckGL with mapStyle |
| GLM 5.3 (8k reasoning cap, see below) | 32/68 | 13 | 3 | 9 | 7 | 1/4 fully, 2/4 partially | 4/8 | 8.9.35, 8.9.30, 8.9.35, 8.9.35 | MapboxOverlay in two files; Mapbox GL JS with a token error in one; hand-rolled TileLayer basemap in one |

Generation time per map: Fable 28–42 s, GPT-5.6-sol 39–68 s, Gemini 3.8 Flash 20–35 s, Gemini 3.1 Pro 34–45 s, GLM 5.3 10–33 s once its reasoning was capped.

## Findings

1. **The maps work.** Sixteen of sixteen files from the four closed frontier models rendered the intended data with zero page errors, zero console errors and zero HTTP errors. Every explicit requirement was met in 14 of 16 cells; the two misses were partial (Fable T1 small-airport points nearly invisible; Gemini 3.8 T2 legend labels rounded so two classes read the same). This is the "pretty impressive usage" result, and the screenshots are presentable as-is.
2. **Cartography is competent but converges on the same defaults.** Every model chose a CARTO basemap unprompted (Positron for light, Dark Matter for dark). Every choropleth used YlOrRd with six quantile classes. Every hexagon map used the colorRange from the official deck.gl example, and three of four left most of the country in the lowest bin because of the long-tailed count distribution. Judge cartography scores sit at 3–4 of 5 for all models; nobody scored a 5. The defects are the ones a human cartographer catches: skew handling, legend labels, small-point visibility, no legend on the trips map.
3. **API currency is the differentiator, and it is low.** Twelve of sixteen closed-model files pin a deck.gl 8.9.x bundle, fifteen of twenty across all five models. Only GPT-5.6-sol used the v9 overlay pattern (MapboxOverlay added with addControl) in every task; Fable used it nowhere despite pinning 9.0.x in two files; both Geminis used the v8 standalone DeckGL class, and Gemini 3.1 Pro used the old `window.mapboxgl = maplibregl` alias hack in all four files. Nobody used 9.2, 9.3 or 9.4. Nobody used the new `@deck.gl/maplibre` module, three days old. Three files used the deprecated `rounded` prop on TripsLayer. Every v8 standalone file also fires a request for a Mapbox CSS file that the browser blocks, a fingerprint of the v8 scripting bundle that costs nothing but shows the pattern's age.
4. **Task type predicts the version.** The hexagon and trips tasks pulled models toward 8.9.x more than the points and choropleth tasks did. Those two are the canonical deck.gl showcase examples, and the training data for them is v8-era code. The model reproduces the example's stack along with its idea.
5. **Speed is not quality.** Gemini 3.8 Flash produced the most code per second and the most polished control panels, and scored lowest on API currency. GPT-5.6-sol took twice as long and scored highest.

## GLM 5.3, the open-weight frontier model

Getting output at all took four attempts. The OpenRouter endpoint makes reasoning mandatory, and with default settings the model spent the entire 24,000-token budget thinking on all four tasks (about 400 s each, no HTML). With `reasoning.effort = low` it spent 40,000 tokens thinking on three of four tasks (about 600 s each); the one map it did finish pinned `deck.gl@8.10.1`, a version that does not exist, so the script never loaded. Disabling reasoning is rejected by the endpoint. Only an explicit `reasoning.max_tokens = 8000` cap produced four files, each in 10–33 s with under 800 reasoning tokens. Earlier attempts are archived in `attempts/`.

The four files scored 32/68, half the closed models. One map is fully correct and pleasant (airports, 13/17, correct MapboxOverlay integration). The other three fail on deck.gl fundamentals rather than on cartography:
- Choropleth: `const deck = new deck.Deck(...)` shadows the library's own global, so no layer is ever created; it also loads Mapbox GL JS, which demands a token, violating the prompt. Blank page.
- Hexagons: instead of a MapLibre basemap it hand-rolls a TileLayer and reads `props.bbox` instead of `props.tile.bbox`, so every tile throws and the hexagons float on black. Twelve-entry colorRange with black and random hues.
- Trips: mutates `layer.props.currentTime` and calls the internal `setState` instead of recreating the layer with new props, so the animation dies on the first frame.

For the talk: the open-weight model knows what a deck.gl map should contain, gets the props vocabulary mostly right, but does not know deck.gl's core contract that layers are immutable and are replaced, not mutated. That contract is exactly the kind of unwritten rule a schema or a skill would carry.

## Caveats

Single sample per cell, default temperature, one judge model with a fixed rubric. The judge is Claude, which could favor Claude output; its per-task notes are quoted in the report so the reasoning can be checked, and the API-currency and version facts are verified mechanically from the files. Headless SwiftShader rendering is slower than a GPU, so the 3-second screenshot sometimes predates data arrival; the 8-second shot is used for thumbnails and the 14-second shot is linked.
