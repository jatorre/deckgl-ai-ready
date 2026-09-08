<!-- model: claude-sonnet-5 | prompt: P6_deckgl_versions | seconds: 10 | backend: claude-cli tools=none -->
Targeting **deck.gl v9.1** (latest stable line as of my knowledge).

## Install

```bash
npm install deck.gl@9.1.0 @deck.gl/core@9.1.0 @deck.gl/layers@9.1.0 @deck.gl/react@9.1.0 mapbox-gl@3.9.0
```

(`deck.gl` alone bundles core, layers, and aggregation-layers — the scoped packages are only needed if you want fine-grained imports.)

## Example (React + MapboxGL basemap)

```jsx
import React from 'react';
import DeckGL from '@deck.gl/react';
import {ScatterplotLayer} from '@deck.gl/layers';
import {Map} from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';

const INITIAL_VIEW_STATE = {
  longitude: -122.41669,
  latitude: 37.7853,
  zoom: 11,
  pitch: 0,
  bearing: 0
};

const DATA = [
  {position: [-122.41669, 37.7853], size: 100},
  {position: [-122.42, 37.79], size: 200}
];

function App() {
  const layer = new ScatterplotLayer({
    id: 'scatterplot-layer',
    data: DATA,
    getPosition: d => d.position,
    getRadius: d => d.size,
    getFillColor: [255, 140, 0],
    radiusMinPixels: 2,
    radiusMaxPixels: 100,
    pickable: true
  });

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller
      layers={[layer]}
    >
      <Map mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json" />
    </DeckGL>
  );
}

export default App;
```

**Notes:**
- v9 requires `react-map-gl` v7+ with the `/mapbox` or `/maplibre` subpath import (no more default export from `react-map-gl`).
- If you don't need a basemap, drop `react-map-gl` and `mapbox-gl` entirely and just render `<DeckGL>` standalone.
- For a non-React/vanilla JS setup, only `deck.gl` is needed — instantiate `new Deck({...})` directly.
