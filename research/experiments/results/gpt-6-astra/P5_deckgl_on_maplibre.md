<!-- model: openai/gpt-6-astra | prompt: P5_deckgl_on_maplibre | seconds: 16 | backend: openrouter | usage: {"prompt_tokens": 46, "completion_tokens": 683, "total_tokens": 729, "cost": 0.03461, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03461, "upstream_inference_prompt_cost": 0.00046, "upstream_inference_completions_cost": 0.03415}, "completion_tokens_details": {"reasoning_tokens": 159, "image_tokens": 0, "audio_tokens": 0}} -->
Use deck.gl’s `MapboxOverlay`, which also supports **MapLibre GL JS**. It synchronizes deck.gl’s camera with the map.

### 1. Install

In an empty directory:

```bash
npm init -y
npm install maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
npm install --save-dev vite
```

### 2. Create `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MapLibre + deck.gl</title>
    <style>
      html, body, #map {
        width: 100%;
        height: 100%;
        margin: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script type="module" src="/main.js"></script>
  </body>
</html>
```

### 3. Create `main.js`

```js
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import {MapboxOverlay} from '@deck.gl/mapbox';
import {ScatterplotLayer} from '@deck.gl/layers';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.42, 37.77],
  zoom: 10
});

const overlay = new MapboxOverlay({
  // Separate canvas above the map; MapLibre handles navigation.
  interleaved: false,
  layers: [
    new ScatterplotLayer({
      id: 'locations',
      data: [
        {position: [-122.42, 37.77]},
        {position: [-122.45, 37.79]}
      ],
      getPosition: d => d.position,
      getFillColor: [255, 80, 40, 200],
      getRadius: 500,
      radiusMinPixels: 6
    })
  ]
});

map.addControl(overlay);
map.addControl(new maplibregl.NavigationControl());
```

### 4. Run

```bash
npx vite
```

Open the printed localhost URL. The demo basemap requires internet access but no API token; the circles render above it.