<!-- model: openai/gpt-6-astra | prompt: P1_large_points | seconds: 19 | backend: openrouter | usage: {"prompt_tokens": 73, "completion_tokens": 802, "total_tokens": 875, "cost": 0.04083, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.04083, "upstream_inference_prompt_cost": 0.00073, "upstream_inference_completions_cost": 0.0401}, "completion_tokens_details": {"reasoning_tokens": 248, "image_tokens": 0, "audio_tokens": 0}} -->
**Use Vite + TypeScript, MapLibre GL JS for the basemap, and deck.gl’s `ScatterplotLayer` for GPU-rendered points.** Connect them with `MapboxOverlay`. Avoid DOM markers and a giant GeoJSON source.

For two million points, serve compact binary data instead of JSON. This example assumes little-endian Float32 triples: `[longitude, latitude, speed]`, with speed in m/s.

```bash
npm install maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
```

```js
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import {MapboxOverlay} from '@deck.gl/mapbox';
import {ScatterplotLayer} from '@deck.gl/layers';

document.body.innerHTML =
  '<div id="map" style="position:fixed;inset:0"></div>';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [0, 20],
  zoom: 2
});

const raw = new Float32Array(
  await (await fetch('/points.bin')).arrayBuffer()
);
const n = raw.length / 3;
const positions = new Float32Array(n * 2);
const colors = new Uint8Array(n * 3);

for (let i = 0; i < n; i++) {
  positions[2 * i] = raw[3 * i];
  positions[2 * i + 1] = raw[3 * i + 1];
  const t = Math.max(0, Math.min(1, raw[3 * i + 2] / 40));
  colors.set([255 * t, 80, 255 * (1 - t)], 3 * i);
}

map.addControl(new MapboxOverlay({
  layers: [new ScatterplotLayer({
    id: 'gps',
    data: {
      length: n,
      attributes: {
        getPosition: {value: positions, size: 2},
        getFillColor: {value: colors, size: 3}
      }
    },
    getRadius: 2,
    radiusUnits: 'pixels',
    pickable: false
  })]
}));
```

**Performance:** Keep buffers static during navigation; preprocess in a worker for nonblocking startup. Benchmark target devices: two million points are GPU-dependent. For mobile or heavy overdraw, add server-generated spatial tiles with zoom-dependent sampling. Replace the demo basemap with a production tile provider.