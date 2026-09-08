<!-- model: claude-haiku-4-5-20251001 | prompt: P5_deckgl_on_maplibre | seconds: 10 | backend: claude-cli tools=none -->
## Install packages

```bash
npm install maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
```

## Minimal code example

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@latest/dist/maplibre-gl.css">
  <style>
    body { margin: 0; }
    #map { width: 100%; height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script type="module">
    import maplibregl from 'maplibre-gl';
    import { ScatterplotLayer } from '@deck.gl/layers';
    import { MapboxOverlay as DeckOverlay } from '@deck.gl/mapbox';

    // Create MapLibre map
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [-74.5, 40],
      zoom: 9
    });

    map.on('load', () => {
      // Sample data
      const data = [
        { position: [-74.5, 40], color: [255, 0, 0] },
        { position: [-73.5, 40.5], color: [0, 255, 0] },
        { position: [-75, 39.5], color: [0, 0, 255] }
      ];

      // Create deck.gl layer
      const layer = new ScatterplotLayer({
        id: 'scatterplot',
        data,
        getPosition: d => d.position,
        getRadius: 100000,
        getColor: d => d.color
      });

      // Add overlay to map
      const overlay = new DeckOverlay({ layers: [layer] });
      overlay.setProps({ layers: [layer] });
      map.addLayer(overlay);
    });
  </script>
</body>
</html>
```

## How it works

1. **MapboxOverlay** wraps deck.gl layers for MapLibre compatibility
2. Pass your deck.gl layers to the overlay
3. Add the overlay to the map with `map.addLayer()`
4. deck.gl layers render on top of MapLibre using WebGL for high performance

You can swap `ScatterplotLayer` for other deck.gl layers like `LineLayer`, `PolygonLayer`, `HeatmapLayer`, etc. All layers accept the same data and styling props.
