<!-- model: claude-opus-5 | prompt: P5_deckgl_on_maplibre | seconds: 16 | backend: claude-cli tools=none -->
## Install

```bash
npm install deck.gl maplibre-gl
```

`deck.gl` is the bundle metapackage (includes `@deck.gl/core`, `@deck.gl/layers`, `@deck.gl/mapbox`). If you prefer scoped packages: `npm install @deck.gl/core @deck.gl/layers @deck.gl/mapbox maplibre-gl`.

## Code

```js
import maplibregl from 'maplibre-gl';
import {MapboxOverlay} from '@deck.gl/mapbox';
import {ScatterplotLayer} from '@deck.gl/layers';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-122.4, 37.79],
  zoom: 11
});

const overlay = new MapboxOverlay({
  interleaved: true,
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data: [
        {position: [-122.42, 37.78], size: 500},
        {position: [-122.39, 37.80], size: 800}
      ],
      getPosition: d => d.position,
      getRadius: d => d.size,
      getFillColor: [255, 100, 0, 180],
      pickable: true
    })
  ]
});

map.on('load', () => map.addControl(overlay));
```

```html
<div id="map" style="width:100%;height:100vh"></div>
```

Despite the name, `MapboxOverlay` works with MapLibre — deck.gl detects which library instantiated the map.

## Key points

- **`interleaved: true`** renders deck.gl layers inside MapLibre's WebGL context, so 3D layers occlude correctly against basemap buildings/labels. Requires the map's style to be loaded, hence `map.on('load', ...)`.
- **`interleaved: false`** (default) draws deck.gl in a separate canvas on top. Simpler and more robust — use it unless you need depth interleaving with basemap geometry.
- **Updating layers:** call `overlay.setProps({layers: [...]})` with new layer instances. Reuse the same layer `id` so deck.gl diffs rather than rebuilds.
- **Layer ordering** in interleaved mode: pass `beforeId: '<maplibre-layer-id>'` on a deck layer to slot it beneath a basemap layer (e.g. under labels).
- MapLibre v4/v5 and deck.gl v9 are the current compatible pairing.
