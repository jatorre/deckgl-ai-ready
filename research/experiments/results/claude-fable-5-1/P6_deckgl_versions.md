<!-- model: claude-fable-5-1 | prompt: P6_deckgl_versions | seconds: 18 | backend: claude-cli tools=none -->
Targeting **deck.gl 9.1** (the newest release I know well as of my cutoff; a later 9.x minor may exist, and these packages are released in lockstep, so pin them to the same version).

Install:

```bash
npm install deck.gl@^9.1.0 @deck.gl/core@^9.1.0 @deck.gl/layers@^9.1.0 @luma.gl/core@^9.1.0 @luma.gl/webgl@^9.1.0
```

Only `@deck.gl/core` and `@deck.gl/layers` are strictly needed. The `deck.gl` umbrella package re-exports them, and the luma.gl packages are peer dependencies that the umbrella pulls in.

Minimal example (vanilla, no React, no basemap):

```js
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer } from '@deck.gl/layers';

const data = [
  { position: [-122.45, 37.78], size: 100 },
  { position: [-122.40, 37.75], size: 200 }
];

const layer = new ScatterplotLayer({
  id: 'scatterplot',
  data,
  getPosition: d => d.position,
  getRadius: d => d.size,
  getFillColor: [255, 140, 0],
  radiusUnits: 'meters',
  pickable: true
});

new Deck({
  initialViewState: {
    longitude: -122.42,
    latitude: 37.77,
    zoom: 11
  },
  controller: true,
  layers: [layer]
});
```

Notes:

- With no `parent` or `canvas` option, Deck creates a full-window canvas. Pass `parent: document.getElementById('app')` to mount into a specific element.
- deck.gl 9 defaults to WebGL2. To use WebGPU, install `@luma.gl/webgpu` and pass `device: {type: 'webgpu'}` to `Deck`, but WebGPU support is still marked experimental in 9.1.
- To add a basemap, install `maplibre-gl` and `@deck.gl/mapbox`, then use `MapboxOverlay` instead of `Deck`.
