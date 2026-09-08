<!-- model: claude-sonnet-5 | prompt: P1_large_points | seconds: 12 | backend: claude-cli tools=none -->
**Recommendation:** Use **deck.gl** (WebGL-powered) on top of **MapLibre GL JS** for the basemap. deck.gl's `ScatterplotLayer` handles millions of points smoothly because it renders directly on the GPU and supports binary typed-array data (avoiding per-point JS object overhead). Pair with `@deck.gl/mapbox` (or `@deck.gl/maplibre`) to sync deck.gl layers with MapLibre's pan/zoom.

For 2M points, load data as flat `Float32Array`s (lng/lat/speed) rather than an array of objects — this is the single biggest lever for keeping it smooth.

```js
import { Map } from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

const map = new Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [0, 0],
  zoom: 2,
});

// positions: Float32Array [lng0,lat0, lng1,lat1, ...]
// speeds: Float32Array [speed0, speed1, ...]
const layer = new ScatterplotLayer({
  id: 'gps-points',
  data: {
    length: positions.length / 2,
    attributes: {
      getPosition: { value: positions, size: 2 },
      getFillColor: {
        value: speedToColor(speeds), // precomputed Uint8Array RGBA per point
        size: 4,
      },
    },
  },
  radiusMinPixels: 1,
  radiusMaxPixels: 4,
  pickable: false, // disable if you don't need hover/click on individual points
});

const overlay = new MapboxOverlay({ layers: [layer] });
map.addControl(overlay);
```

Key perf tips:
- Precompute `getFillColor` as a `Uint8Array` (speed → RGBA ramp) once, not per render.
- Set `pickable: false` unless you need per-point interaction — picking adds overhead.
- Consider `radiusUnits: 'pixels'` and clamp min/max radius so zoomed-out views don't overdraw.
- If you need aggregation at low zoom, swap in `HeatmapLayer` or `HexagonLayer` above a zoom threshold.

This stack (MapLibre + deck.gl) is the standard choice for large-scale geospatial point rendering in the browser and is actively maintained.
