<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P6_deckgl_versions | seconds: 5 | backend: litellm-proxy | usage: {"completion_tokens": 323, "prompt_tokens": 55, "total_tokens": 378, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Targeting **deck.gl v9.0.0** (latest I know).

### Install (exact versions)
```bash
npm i deck.gl@9.0.0 @deck.gl/core@9.0.0 @deck.gl/layers@9.0.0
```

### Minimal ScatterplotLayer (ESM)
```js
import {Deck} from '@deck.gl/core';
import {ScatterplotLayer} from '@deck.gl/layers';

const data = [
  {position: [-122.41669, 37.7853], size: 100},
  {position: [-122.40669, 37.7810], size: 60}
];

const deck = new Deck({
  container: 'deck-container', // <div id="deck-container"></div>
  initialViewState: {
    longitude: -122.412,
    latitude: 37.783,
    zoom: 12,
    pitch: 0,
    bearing: 0
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      id: 'scatter',
      data,
      getPosition: d => d.position,
      getRadius: d => d.size,     // meters by default
      radiusMinPixels: 3,
      getFillColor: [0, 128, 255, 180],
      pickable: true
    })
  ]
});
```

### Minimal HTML container
```html
<div id="deck-container" style="position:fixed; inset:0;"></div>
```