<!-- model: claude-opus-5 | prompt: P1_large_points | seconds: 18 | backend: claude-cli tools=none -->
## Recommendation: MapLibre GL JS + deck.gl, with typed-array (binary) attributes

deck.gl renders 2M points in one WebGL draw call; MapLibre supplies the basemap. Keep data as `Float32Array`/`Uint8Array` — passing an array of 2M JS objects is what actually kills performance.

```js
import maplibregl from 'maplibre-gl';
import {MapboxOverlay} from '@deck.gl/mapbox';
import {ScatterplotLayer} from '@deck.gl/layers';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-3.7, 40.4], zoom: 10
});

// Fetch precomputed binary buffers: lon/lat pairs + RGB per point.
const [positions, colors] = await Promise.all([
  fetch('/points.f32').then(r => r.arrayBuffer()).then(b => new Float32Array(b)),
  fetch('/speed_rgb.u8').then(r => r.arrayBuffer()).then(b => new Uint8Array(b))
]);

const overlay = new MapboxOverlay({
  interleaved: true,
  layers: [new ScatterplotLayer({
    id: 'gps',
    data: {
      length: positions.length / 2,
      attributes: {
        getPosition: {value: positions, size: 2},
        getFillColor: {value: colors, size: 3, normalized: false}
      }
    },
    radiusUnits: 'pixels',
    getRadius: 1.5,
    radiusMinPixels: 1,
    pickable: false   // picking on 2M points costs a second render pass
  })]
});

map.addControl(overlay);
```

**Pipeline:** convert your CSV/Parquet once (Python/DuckDB) into two raw binary files — interleaved `lon,lat` floats and an RGB byte per point from your speed ramp. That's ~22 MB, gzip-served, one fetch, zero per-point JS work.

**Scaling notes:** `interleaved: true` puts points *under* basemap labels. If you grow past ~10M points or want server-side filtering, switch to spatially-partitioned tiles with `MVTLayer`, or `GeoArrowScatterplotLayer` if you keep Arrow end-to-end. For dense zoomed-out views, a `ScreenGridLayer`/`HeatmapLayer` toggle reads better than overplotted dots.
