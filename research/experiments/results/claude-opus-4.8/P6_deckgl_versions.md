<!-- model: anthropic/claude-opus-4.8 | prompt: P6_deckgl_versions | seconds: 9 | backend: openrouter | usage: {"prompt_tokens": 84, "completion_tokens": 717, "total_tokens": 801, "cost": 0.018345, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.018345, "upstream_inference_prompt_cost": 0.00042, "upstream_inference_completions_cost": 0.017925}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Minimal deck.gl ScatterplotLayer Example

**Targeting deck.gl version: `9.0.x`**

## NPM Packages to Install

```bash
npm install deck.gl@^9.0.0
```

The `deck.gl` meta-package bundles the core modules (`@deck.gl/core`, `@deck.gl/layers`, `@deck.gl/react`, etc.). If you prefer submodules:

```bash
npm install @deck.gl/core@^9.0.0 @deck.gl/layers@^9.0.0
```

## Example (vanilla JS / standalone Deck)

```js
import {Deck} from '@deck.gl/core';
import {ScatterplotLayer} from '@deck.gl/layers';

const data = [
  {position: [-122.45, 37.78], size: 100, color: [255, 0, 0]},
  {position: [-122.44, 37.79], size: 150, color: [0, 128, 255]}
];

const scatterplotLayer = new ScatterplotLayer({
  id: 'scatterplot-layer',
  data,
  getPosition: d => d.position,
  getRadius: d => d.size,
  getFillColor: d => d.color,
  radiusUnits: 'meters',
  pickable: true
});

new Deck({
  initialViewState: {
    longitude: -122.45,
    latitude: 37.78,
    zoom: 13
  },
  controller: true,
  layers: [scatterplotLayer]
});
```

## Notes

- This uses `Deck` directly (no basemap required). It renders into a full-screen canvas by default.
- To add an HTML container, pass `parent: document.getElementById('app')` or `canvas: 'my-canvas'` to the `Deck` constructor.
- For React, install `@deck.gl/react@^9.0.0` and use the `<DeckGL>` component with the same `layers` prop.

The `ScatterplotLayer` API (props like `getPosition`, `getFillColor`, `getRadius`) is stable across deck.gl 8.x and 9.x, so this example works with minor changes on `8.9.x` too.