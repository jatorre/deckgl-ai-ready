<!-- model: claude-sonnet-5 | prompt: P5_deckgl_on_maplibre | seconds: 10 | backend: claude-cli tools=none -->
## Install

```bash
npm install maplibre-gl deck.gl
```

## Minimal example

```js
import maplibregl from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [0, 0],
  zoom: 2
});

map.on('load', () => {
  const overlay = new MapboxOverlay({
    interleaved: true,
    layers: [
      new ScatterplotLayer({
        id: 'points',
        data: [
          { position: [0, 0], size: 100 },
          { position: [10, 10], size: 200 }
        ],
        getPosition: d => d.position,
        getRadius: d => d.size,
        getFillColor: [255, 0, 0],
        radiusUnits: 'meters'
      })
    ]
  });

  map.addControl(overlay);
});
```

```html
<div id="map" style="width: 100%; height: 100vh;"></div>
```

**Key points:**
- `@deck.gl/mapbox` provides `MapboxOverlay`, which works with MapLibre GL JS despite the package name (both share the same GL JS API surface).
- Setting `interleaved: true` lets deck.gl layers render interleaved with MapLibre's own layers (correct depth sorting with 3D buildings, etc.). Omit it (or set `false`) for a simpler overlay-on-top approach, which is faster but always draws deck.gl layers above the base map.
- Add the overlay only after `map.on('load')` fires so the map's WebGL context is ready.
- `deck.gl` is the umbrella package (pulls in `@deck.gl/core`, `@deck.gl/layers`, etc.); you can also install only the sub-packages you need (`@deck.gl/core`, `@deck.gl/layers`, `@deck.gl/mapbox`) for a smaller bundle.
