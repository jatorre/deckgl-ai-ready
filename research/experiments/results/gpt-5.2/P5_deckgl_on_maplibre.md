<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P5_deckgl_on_maplibre | seconds: 9 | backend: litellm-proxy | usage: {"completion_tokens": 419, "prompt_tokens": 46, "total_tokens": 465, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Install packages:

```bash
npm i maplibre-gl deck.gl
# or: npm i maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/mapbox
```

Minimal complete example (MapLibre + deck.gl overlay using `MapboxOverlay`, which works with MapLibre via the Mapbox-compatible API):

```js
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

import {MapboxOverlay} from "@deck.gl/mapbox";
import {ScatterplotLayer} from "@deck.gl/layers";

const map = new maplibregl.Map({
  container: "map",
  style: "https://demotiles.maplibre.org/style.json",
  center: [-122.4, 37.78],
  zoom: 11
});

map.on("load", () => {
  const deckOverlay = new MapboxOverlay({
    interleaved: true, // share WebGL context with the map
    layers: [
      new ScatterplotLayer({
        id: "points",
        data: [
          {position: [-122.401, 37.785], size: 200},
          {position: [-122.411, 37.775], size: 400}
        ],
        getPosition: d => d.position,
        getRadius: d => d.size,
        radiusMinPixels: 3,
        getFillColor: [255, 0, 0, 180],
        pickable: true
      })
    ]
  });

  map.addControl(deckOverlay);

  // later updates (optional):
  // deckOverlay.setProps({ layers: [...] });
});
```

HTML:

```html
<div id="map" style="position:fixed; inset:0;"></div>
<script type="module" src="/main.js"></script>
```

This renders a deck.gl `ScatterplotLayer` on top of the MapLibre map, sharing the same WebGL context for better performance.