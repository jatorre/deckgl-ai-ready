<!-- model: claude-opus-5 | prompt: P3_h3_hexagons | seconds: 16 | backend: claude-cli tools=none -->
## Recommendation

**deck.gl** with `H3HexagonLayer` — it decodes H3 indexes to boundaries on the GPU, so you skip converting cells to GeoJSON. Pair it with **MapLibre GL JS** (free, no token) for the basemap, and **d3-scale-chromatic** for the color ramp.

```bash
npm i deck.gl maplibre-gl d3-scale d3-scale-chromatic
```

```js
import { Deck } from '@deck.gl/core';
import { H3HexagonLayer } from '@deck.gl/geo-layers';
import maplibregl from 'maplibre-gl';
import { scaleSequential } from 'd3-scale';
import { interpolateViridis } from 'd3-scale-chromatic';
import 'maplibre-gl/dist/maplibre-gl.css';

// [{ h3: '8a2a1072b59ffff', count: 42 }, ...]
const data = await fetch('/hexes.json').then(r => r.json());

const max = Math.max(...data.map(d => d.count));
const color = scaleSequential(interpolateViridis).domain([0, max]);
const rgb = c => {
  const [, r, g, b] = color(c).match(/\d+/g).map(Number) ? [] : [];
  const m = color(c).match(/\d+/g).map(Number);
  return [m[0], m[1], m[2]];
};

const INITIAL_VIEW_STATE = { longitude: -3.70, latitude: 40.42, zoom: 11 };

new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  ...INITIAL_VIEW_STATE
});

new Deck({
  canvas: 'deck-canvas',
  initialViewState: INITIAL_VIEW_STATE,
  controller: true,
  layers: [
    new H3HexagonLayer({
      id: 'hexes',
      data,
      getHexagon: d => d.h3,
      getFillColor: d => rgb(d.count),
      getLineColor: [255, 255, 255, 40],
      extruded: false,
      pickable: true,
      opacity: 0.8
    })
  ],
  getTooltip: ({ object }) => object && `${object.h3}: ${object.count}`
});
```

HTML needs a `#map` div with a `#deck-canvas` overlaid on it (absolute positioning); deck.gl's docs show the exact pattern for syncing the two view states.

Notes: the `rgb` helper above is clumsier than needed — cleaner to precompute an `[r,g,b]` array per row once, since `getFillColor` runs per feature. For >1M cells, switch to binary attributes or aggregate to a coarser H3 resolution before rendering. If your data lives in a warehouse, `@deck.gl/carto`'s `h3QuerySource` handles tiling server-side.
