<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P5_deckgl_on_maplibre | seconds: 5 | backend: litellm-proxy | usage: {"completion_tokens": 739, "prompt_tokens": 44, "total_tokens": 783, "completion_tokens_details": {"reasoning_tokens": 300, "text_tokens": 439}, "prompt_tokens_details": {"text_tokens": 44}} -->
### NPM Packages

Install the required packages (`@deck.gl/mapbox` provides the `MapboxOverlay` control which is fully compatible with MapLibre):

```bash
npm install maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
```

### Minimal Code Example

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

// 1. Initialize the MapLibre map
const map = new maplibregl.Map({
  container: 'map', // Ensure an element with id="map" exists with set height/width
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4, 37.74],
  zoom: 11
});

// 2. Define a deck.gl layer
const scatterLayer = new ScatterplotLayer({
  id: 'deckgl-scatter',
  data: [{ position: [-122.4, 37.74], size: 100 }],
  getPosition: d => d.position,
  getRadius: d => d.size,
  getFillColor: [255, 0, 0, 200],
  radiusMinPixels: 10
});

// 3. Create the deck.gl MapboxOverlay
const deckOverlay = new MapboxOverlay({
  layers: [scatterLayer]
});

// 4. Add the deck overlay as a MapLibre control
map.addControl(deckOverlay);
```

### HTML Setup

Ensure your HTML includes a container for the map:

```html
<div id="map" style="width: 100vw; height: 100vh;"></div>
```