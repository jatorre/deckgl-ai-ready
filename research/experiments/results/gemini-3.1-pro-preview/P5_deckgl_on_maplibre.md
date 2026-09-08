<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P5_deckgl_on_maplibre | seconds: 14 | backend: litellm-proxy max_tokens=12000 | usage: {"completion_tokens": 1873, "prompt_tokens": 44, "total_tokens": 1917, "completion_tokens_details": {"reasoning_tokens": 1328, "text_tokens": 545}, "prompt_tokens_details": {"text_tokens": 44}} -->
To seamlessly integrate deck.gl with MapLibre GL JS, use deck.gl's `MapboxOverlay`. This keeps the cameras perfectly synchronized and allows them to share a WebGL context.

### 1. Install npm packages
```bash
npm install maplibre-gl deck.gl
```

### 2. Complete Minimal Example
Make sure your HTML includes a map container:
```html
<div id="map" style="width: 100vw; height: 100vh; margin: 0;"></div>
```

Here is the complete JavaScript code to initialize the map and add a deck.gl scatterplot layer:

```javascript
import 'maplibre-gl/dist/maplibre-gl.css';
import maplibregl from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

// 1. Initialize MapLibre GL JS
const map = new maplibregl.Map({
  container: 'map',
  // Free public base map style
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-122.4, 37.74],
  zoom: 11,
  pitch: 30
});

// 2. Create the deck.gl overlay
const deckOverlay = new MapboxOverlay({
  interleaved: true, // Allows deck.gl layers to intertwine with MapLibre layers
  layers: [
    new ScatterplotLayer({
      id: 'my-scatterplot',
      data: [
        { position: [-122.4, 37.74], radius: 1000 }
      ],
      getPosition: d => d.position,
      getRadius: d => d.radius,
      getFillColor: [255, 0, 0, 200],
      radiusMinPixels: 10
    })
  ]
});

// 3. Add the deck.gl overlay to the map as a control
map.addControl(deckOverlay);
```

**Why this works:** MapLibre is a fork of Mapbox GL JS. Because their plugin APIs are identical, deck.gl's `@deck.gl/mapbox` module works perfectly with MapLibre out of the box using the `.addControl()` method.