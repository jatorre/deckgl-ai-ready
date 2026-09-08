<!-- model: claude-fable-5-1 | prompt: P5_deckgl_on_maplibre | seconds: 18 | backend: claude-cli tools=none -->
Install:

```bash
npm install maplibre-gl deck.gl
```

The `deck.gl` package bundles `@deck.gl/core`, `@deck.gl/layers`, and `@deck.gl/mapbox`. The MapboxOverlay class in that last module works with MapLibre as a native control.

```js
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-3.7, 40.4],
  zoom: 11
});

const overlay = new MapboxOverlay({
  interleaved: true,
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data: [
        { position: [-3.7038, 40.4168], size: 400 },
        { position: [-3.6883, 40.4530], size: 250 }
      ],
      getPosition: d => d.position,
      getRadius: d => d.size,
      getFillColor: [255, 0, 128, 180],
      pickable: true
    })
  ]
});

map.addControl(overlay);

// Update layers later with:
// overlay.setProps({ layers: [...] });
```

HTML needs a container:

```html
<div id="map" style="width: 100vw; height: 100vh;"></div>
```

Two rendering modes:

- **interleaved: true** draws deck.gl into MapLibre's WebGL context. Labels and 3D buildings can sit above your layer using the `beforeId` prop on each layer.
- **interleaved: false** (the default) renders deck.gl in a separate canvas on top. It is simpler and avoids context sharing edge cases, but everything draws above the basemap.

Picking, tooltips, and view state sync are handled by the overlay. Call `overlay.setProps` whenever data changes rather than creating a new overlay.
