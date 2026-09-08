<!-- model: google/gemini-3.8-flash | prompt: P6_deckgl_versions | seconds: 6 | backend: openrouter | usage: {"prompt_tokens": 54, "completion_tokens": 851, "total_tokens": 905, "cost": 0.00323175, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.00323175, "upstream_inference_prompt_cost": 4.05e-05, "upstream_inference_completions_cost": 0.00319125}, "completion_tokens_details": {"reasoning_tokens": 522, "image_tokens": 0, "audio_tokens": 0}} -->
### Target Version
deck.gl **v9.0** (v9.0.38)

### NPM Packages
Install using npm:

```bash
npm install @deck.gl/core@^9.0.0 @deck.gl/layers@^9.0.0
```

### Minimal Example

```javascript
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer } from '@deck.gl/layers';

const data = [
  { coordinates: [-122.4194, 37.7749], radius: 100 }, // San Francisco
  { coordinates: [-122.4500, 37.7600], radius: 150 }
];

new Deck({
  initialViewState: {
    longitude: -122.42,
    latitude: 37.77,
    zoom: 12,
    pitch: 0,
    bearing: 0
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      id: 'scatter-layer',
      data,
      getPosition: d => d.coordinates,
      getRadius: d => d.radius,
      getFillColor: [255, 0, 128, 200],
      radiusMinPixels: 6,
      pickable: true
    })
  ]
});
```