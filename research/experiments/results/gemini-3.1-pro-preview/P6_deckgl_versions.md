<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P6_deckgl_versions | seconds: 12 | backend: litellm-proxy | usage: {"completion_tokens": 1545, "prompt_tokens": 54, "total_tokens": 1599, "completion_tokens_details": {"reasoning_tokens": 1021, "text_tokens": 524}, "prompt_tokens_details": {"text_tokens": 54}} -->
**Target deck.gl version:** 9.0.0 (React environment)

### 1. Installation
Install the exact required packages using npm:
```bash
npm install @deck.gl/react@9.0.0 @deck.gl/layers@9.0.0 react@18.2.0 react-dom@18.2.0
```

### 2. Code Example
Here is a minimal, self-contained React component rendering a `ScatterplotLayer` (no external basemap required).

```jsx
import React from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

// Minimal dataset
const data = [
  { position: [-122.45, 37.8], color: [255, 0, 0], radius: 1000 },
  { position: [-122.41, 37.79], color: [0, 128, 255], radius: 800 }
];

// Initial map camera settings
const INITIAL_VIEW_STATE = {
  longitude: -122.43,
  latitude: 37.8,
  zoom: 11,
  pitch: 0,
  bearing: 0
};

export default function MinimalScatterplot() {
  // Define the ScatterplotLayer
  const layer = new ScatterplotLayer({
    id: 'scatter-layer',
    data,
    pickable: true,
    opacity: 0.8,
    stroked: false,
    filled: true,
    radiusScale: 1,
    radiusMinPixels: 5,
    radiusMaxPixels: 50,
    getPosition: d => d.position,
    getFillColor: d => d.color,
    getRadius: d => d.radius
  });

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers={[layer]}
    />
  );
}
```

### Notes
* `controller={true}` allows users to pan and zoom the visualization.
* Accessors like `getPosition`, `getFillColor`, and `getRadius` tell deck.gl how to read your specific data structure.