<!-- model: google/gemini-3.8-flash | prompt: P5_deckgl_on_maplibre | seconds: 5 | backend: openrouter | usage: {"prompt_tokens": 44, "completion_tokens": 741, "total_tokens": 785, "cost": 0.00281175, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.00281175, "upstream_inference_prompt_cost": 3.3e-05, "upstream_inference_completions_cost": 0.00277875}, "completion_tokens_details": {"reasoning_tokens": 247, "image_tokens": 0, "audio_tokens": 0}} -->
### NPM Packages

Install `maplibre-gl` and the required deck.gl modules:

```bash
npm install maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
```

*(You must also include the MapLibre CSS file in your project or HTML: `maplibre-gl/dist/maplibre-gl.css`)*

---

### Minimal Example

Use `MapboxOverlay` from `@deck.gl/mapbox`, which is fully compatible with MapLibre via `map.addControl()`.

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

// 1. Initialize the MapLibre map
const map = new maplibregl.Map({
  container: 'map', // Ensure a <div id="map" style="width: 100vw; height: 100vh;"></div> exists
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4, 37.74],
  zoom: 11
});

// 2. Define the deck.gl layer
const scatterLayer = new ScatterplotLayer({
  id: 'scatter-layer',
  data: [
    { position: [-122.4, 37.74], size: 100 }
  ],
  getPosition: d => d.position,
  getRadius: d => d.size,
  getFillColor: [255, 0, 0],
  radiusMinPixels: 10
});

// 3. Create the deck.gl overlay
const deckOverlay = new MapboxOverlay({
  layers: [scatterLayer]
});

// 4. Add the overlay to MapLibre
map.addControl(deckOverlay);
```

### Dynamic Updates
To update layers dynamically later, call:

```javascript
deckOverlay.setProps({
  layers: [/* new/updated layers */]
});
```