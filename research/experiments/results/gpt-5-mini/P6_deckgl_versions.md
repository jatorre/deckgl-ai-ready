<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P6_deckgl_versions | seconds: 18 | backend: litellm-proxy | usage: {"completion_tokens": 1727, "prompt_tokens": 55, "total_tokens": 1782, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 1344, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Targeting deck.gl v8.10.8 (latest I know as of 2024-06).

Install (exact packages/versions):
npm install react@18.2.0 react-dom@18.2.0 @deck.gl/core@8.10.8 @deck.gl/react@8.10.8 @deck.gl/layers@8.10.8

Imports and minimal example (React 18):
```js
import React from 'react';
import { createRoot } from 'react-dom/client';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

const data = [
  { position: [-122.45, 37.78], size: 100 },
  { position: [-122.46, 37.76], size: 200 }
];

const initialViewState = {
  longitude: -122.45,
  latitude: 37.77,
  zoom: 12,
  pitch: 0,
  bearing: 0
};

function App() {
  const layers = [
    new ScatterplotLayer({
      id: 'scatter',
      data,
      getPosition: d => d.position,
      getRadius: d => d.size,
      radiusScale: 1,
      getFillColor: [255, 140, 0],
      pickable: true
    })
  ];

  return (
    <DeckGL initialViewState={initialViewState} controller={true} layers={layers} />
  );
}

createRoot(document.getElementById('root')).render(<App />);
```

Notes: this example uses DeckGL without a basemap. To add a map background, install and include a map provider (react-map-gl / Mapbox or MapLibre) and pass it as a child of DeckGL.