<!-- model: anthropic/claude-opus-4.8 | prompt: P5_deckgl_on_maplibre | seconds: 9 | backend: openrouter | usage: {"prompt_tokens": 66, "completion_tokens": 782, "total_tokens": 848, "cost": 0.01988, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.01988, "upstream_inference_prompt_cost": 0.00033, "upstream_inference_completions_cost": 0.01955}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Adding a deck.gl Layer to MapLibre GL JS

## Install Packages

```bash
npm install maplibre-gl deck.gl @deck.gl/mapbox
```

- `maplibre-gl` — the base map
- `deck.gl` — the layers and core
- `@deck.gl/mapbox` — the `MapboxOverlay` interop class that works with MapLibre

## Complete Minimal Example

```javascript
import maplibregl from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';
import 'maplibre-gl/dist/maplibre-gl.css';

// 1. Create the MapLibre map
const map = new maplibregl.Map({
  container: 'map', // id of a <div> in your HTML
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4, 37.74],
  zoom: 11
});

// 2. Create a deck.gl overlay with a layer
const overlay = new MapboxOverlay({
  layers: [
    new ScatterplotLayer({
      id: 'my-scatter',
      data: [
        { position: [-122.4, 37.74], size: 1000 },
        { position: [-122.45, 37.78], size: 1500 }
      ],
      getPosition: d => d.position,
      getRadius: d => d.size,
      getFillColor: [255, 0, 0, 180],
      radiusMinPixels: 5
    })
  ]
});

// 3. Add the overlay as a MapLibre control
map.addControl(overlay);
```

Required HTML:

```html
<div id="map" style="width: 100vw; height: 100vh;"></div>
```

## Key Points

- `MapboxOverlay` works with MapLibre despite the name — the APIs are compatible.
- Use `map.addControl(overlay)` to attach it; the overlay syncs its camera with the map automatically.
- To update layers later, call `overlay.setProps({ layers: [...] })`.
- For `interleaved: true` (rendering deck.gl layers between map layers), pass it in the `MapboxOverlay` constructor.

This renders two red circles over San Francisco, synced perfectly with map pan/zoom.