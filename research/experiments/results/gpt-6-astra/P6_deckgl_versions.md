<!-- model: openai/gpt-6-astra | prompt: P6_deckgl_versions | seconds: 16 | backend: openrouter | usage: {"prompt_tokens": 55, "completion_tokens": 608, "total_tokens": 663, "cost": 0.03095, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03095, "upstream_inference_prompt_cost": 0.00055, "upstream_inference_completions_cost": 0.0304}, "completion_tokens_details": {"reasoning_tokens": 193, "image_tokens": 0, "audio_tokens": 0}} -->
**Target: deck.gl 9.1.0.** This is the latest version I can confidently target here; I can’t verify the current npm release.

In an existing npm project with a browser bundler, install these exact packages:

```bash
npm install --save-exact @deck.gl/core@9.1.0 @deck.gl/layers@9.1.0
```

**HTML**
```html
<body style="margin: 0">
  <canvas id="deck-canvas"></canvas>
  <script type="module" src="/src/main.js"></script>
</body>
```

**`src/main.js`**
```js
import {Deck} from '@deck.gl/core';
import {ScatterplotLayer} from '@deck.gl/layers';

const data = [
  {position: [-122.41669, 37.7853], radius: 200},
  {position: [-122.40669, 37.7813], radius: 120}
];

new Deck({
  canvas: 'deck-canvas',
  width: '100%',
  height: '100%',
  initialViewState: {
    longitude: -122.412,
    latitude: 37.783,
    zoom: 13,
    pitch: 0,
    bearing: 0
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data,
      getPosition: d => d.position,
      getRadius: d => d.radius,
      radiusUnits: 'meters',
      getFillColor: [255, 100, 50, 200],
      pickable: true
    })
  ],
  getTooltip: ({object}) =>
    object && `Radius: ${object.radius} m`
});
```

This renders two geographic circles with pan/zoom controls and hover tooltips. Positions use **[longitude, latitude]**. No basemap, React, or map-service token is required.