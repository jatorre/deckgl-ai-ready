<!-- model: claude-haiku-4-5-20251001 | prompt: P6_deckgl_versions | seconds: 10 | backend: claude-cli tools=none -->
# Minimal deck.gl ScatterplotLayer Example

**Target Version:** deck.gl 8.12.0

## npm Packages

```bash
npm install deck.gl@8.12.0 @deck.gl/core@8.12.0 @deck.gl/layers@8.12.0
```

## Code Example

```javascript
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer } from '@deck.gl/layers';

// Sample data
const data = [
  { position: [-122.4194, 37.7749], size: 100 },
  { position: [-118.2437, 34.0522], size: 150 },
  { position: [-87.6298, 41.8781], size: 120 },
];

// Create the layer
const scatterplotLayer = new ScatterplotLayer({
  id: 'scatterplot-layer',
  data,
  pickable: true,
  radiusScale: 6,
  getPosition: d => d.position,
  getRadius: d => d.size,
  getColor: [255, 0, 0, 200],
});

// Initialize deck
const deck = new Deck({
  canvas: 'canvas',
  initialViewState: {
    longitude: -95,
    latitude: 40,
    zoom: 3,
  },
  controller: true,
  layers: [scatterplotLayer],
});
```

## HTML Template

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      body { margin: 0; }
      canvas { width: 100%; height: 100vh; }
    </style>
  </head>
  <body>
    <canvas id="canvas"></canvas>
    <script src="app.js"></script>
  </body>
</html>
```

## Key Points

- **@deck.gl/core**: Core Deck and layer management
- **@deck.gl/layers**: Pre-built layer types (ScatterplotLayer)
- Positions use `[longitude, latitude]` format
- Customize colors, sizes, and interactions via layer props
- `controller: true` enables pan/zoom with mouse/touch

This renders red circles at three US cities with zoom/pan controls enabled.
