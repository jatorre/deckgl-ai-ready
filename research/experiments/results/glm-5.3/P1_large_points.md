<!-- model: z-ai/glm-5.3 | prompt: P1_large_points | seconds: 36 | backend: openrouter | usage: {"prompt_tokens": 78, "completion_tokens": 564, "total_tokens": 642, "cost": 0.002450145, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.002450145, "upstream_inference_prompt_cost": 9.2625e-05, "upstream_inference_completions_cost": 0.00235752}, "completion_tokens_details": {"reasoning_tokens": 47, "image_tokens": 0, "audio_tokens": 0}} -->
**Recommendation: MapLibre GL JS + deck.gl (ScatterplotLayer)**

This stack handles millions of points because deck.gl renders via WebGL in batches, keeping the main thread free during pan/zoom.

**Stack:**
- **Basemap:** MapLibre GL JS with free tiles (e.g., OSM raster or a vector tile provider)
- **Points:** deck.gl `ScatterplotLayer` (WebGL, GPU-accelerated)
- **Data format:** Flat binary arrays (Float32Array for lng/lat/speed) — avoid 2M JS objects; if source is CSV/GeoJSON, preprocess once to Parquet or Arrow

```js
import { MaplibreOverlay } from "@deck.gl/mapbox";
import { ScatterplotLayer } from "@deck.gl/layers";

// points: preprocessed binary arrays (length N)
// lons: Float32Array, lats: Float32Array, speeds: Float32Array
const data = lons.map((lon, i) => ({
  coordinates: [lon, lats[i]],
  speed: speeds[i]
}));

const map = new maplibregl.Map({
  container: "map",
  style: "https://demotiles.maplibre.org/style.json",
  center: [-122.4, 37.8],
  zoom: 10
});

const scatter = new ScatterplotLayer({
  id: "gps-points",
  data,
  getPosition: d => d.coordinates,
  getRadius: 20,
  radiusUnits: "meters",
  getFillColor: d => speedToColor(d.speed), // e.g., interpolate red→green
  radiusMinPixels: 1,
  stroked: false,
  pickable: false // set true only if you need tooltips
});

map.addControl(new MaplibreOverlay({ layers: [scatter] }));
```

**Key tips:**
- Set `pickable: false` unless needed — picking 2M points is expensive.
- Use `extensions` with `DataFilterExtension` if filtering by speed range interactively.
- If data is static, serve it as a single gzip-compressed binary file (~2M points ≈ 30–50 MB in Arrow, much less gzipped).
- Alternative if you want tile-based loading: ` loaders.gl` + MVT-based point tiles with GeoParquet, but for a fixed 2M-point dataset, one bulk load into deck.gl is simpler and fast enough.