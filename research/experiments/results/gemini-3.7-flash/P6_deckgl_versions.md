<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P6_deckgl_versions | seconds: 7 | backend: litellm-proxy | usage: {"completion_tokens": 972, "prompt_tokens": 54, "total_tokens": 1026, "completion_tokens_details": {"reasoning_tokens": 645, "text_tokens": 327}, "prompt_tokens_details": {"text_tokens": 54}} -->
### Target Version
**deck.gl v9.1** (targeting `9.1.4`)

---

### Installation
```bash
npm install deck.gl@9.1.4
```

---

### Minimal Example

```javascript
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer } from '@deck.gl/layers';

// 1. Define sample data
const data = [
  { position: [-122.45, 37.8], color: [255, 0, 0], radius: 300 },
  { position: [-122.42, 37.78], color: [0, 128, 255], radius: 500 }
];

// 2. Instantiate the ScatterplotLayer
const layer = new ScatterplotLayer({
  id: 'scatterplot-layer',
  data,
  getPosition: d => d.position,
  getFillColor: d => d.color,
  getRadius: d => d.radius,
  radiusUnits: 'meters',
  pickable: true
});

// 3. Initialize Deck.gl
new Deck({
  initialViewState: {
    longitude: -122.435,
    latitude: 37.79,
    zoom: 12
  },
  controller: true,
  layers: [layer]
});
```