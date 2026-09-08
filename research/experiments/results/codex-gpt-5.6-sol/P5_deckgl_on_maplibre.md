<!-- model: gpt-5.6-sol | prompt: P5_deckgl_on_maplibre | seconds: 65 | backend: codex-cli sandbox=read-only web_search=disabled -->
Install the runtime packages plus Vite:

```bash
npm install maplibre-gl @deck.gl/maplibre @deck.gl/layers
npm install --save-dev vite
```

`index.html`:

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <style>
      html, body, #map { margin: 0; width: 100%; height: 100%; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script type="module" src="/main.js"></script>
  </body>
</html>
```

`main.js`:

```js
import {Map, setWorkerUrl} from 'maplibre-gl';
import workerUrl from
  'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import 'maplibre-gl/dist/maplibre-gl.css';

import {MapLibreOverlay} from '@deck.gl/maplibre';
import {ScatterplotLayer} from '@deck.gl/layers';

setWorkerUrl(workerUrl);

const map = new Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-74.006, 40.7128],
  zoom: 11
});

await map.once('load');

const overlay = new MapLibreOverlay({
  // Separate canvas above the MapLibre map:
  interleaved: false,
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data: [{position: [-74.006, 40.7128]}],
      getPosition: d => d.position,
      getRadius: 500,
      getFillColor: [255, 60, 60, 180],
      pickable: true
    })
  ]
});

map.addControl(overlay);
```

Run it:

```bash
npx vite
```

Use `interleaved: true` instead if deck.gl layers must be positioned among MapLibre style layers; that requires WebGL2. [Official integration guide](https://deck.gl/docs/developer-guide/base-maps/using-with-maplibre)