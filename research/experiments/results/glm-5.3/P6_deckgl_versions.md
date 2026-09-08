<!-- model: z-ai/glm-5.3 | prompt: P6_deckgl_versions | seconds: 11 | backend: openrouter | usage: {"prompt_tokens": 61, "completion_tokens": 575, "total_tokens": 636, "cost": 0.0026154, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0026154, "upstream_inference_prompt_cost": 8.54e-05, "upstream_inference_completions_cost": 0.00253}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# deck.gl ScatterplotLayer — Minimal Example

**Targeting: deck.gl v9.x (tested against 9.1.x)**

## Install

```bash
npm install deck.gl@^9.1.0
```

That's it — deck.gl v9 bundles everything you need in a single package (no separate `@deck.gl/core`, `@deck.gl/layers` installs required, though those subpath imports still work).

## Code

```jsx
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { Map } from 'react-map-gl';
import 'react-map-gl/dist/mapbox-gl.css';

const data = [
  { position: [-122.45, 37.78], size: 200, color: [255, 100, 0] },
  { position: [-122.42, 37.76], size: 300, color: [0, 150, 255] },
];

function App() {
  const layer = new ScatterplotLayer({
    id: 'scatter-layer',
    data,
    getPosition: d => d.position,
    getRadius: d => d.size,
    getFillColor: d => d.color,
    radiusUnits: 'meters',
    pickable: true,
  });

  return (
    <DeckGL
      initialViewState={{ longitude: -122.45, latitude: 37.78, zoom: 12 }}
      controller
      layers={[layer]}
      getTooltip={({ object }) => object && `Size: ${object.size}`}
    >
      <Map
        mapboxAccessToken="<YOUR_TOKEN>"
        mapStyle="mapbox://styles/mapbox/dark-v11"
      />
    </DeckGL>
  );
}

export default App;
```

## Packages

- `deck.gl@^9.1.0` (includes `@deck.gl/core`, `@deck.gl/layers`, `@deck.gl/react`)
- `react-map-gl@^7.1.0` (only needed if you want a basemap)
- `mapbox-gl@^3.0.0` (peer dep of react-map-gl v7)

## Notes

- In deck.gl v9, layers expect GeoJSON/web-mercator coordinates by default (same as v8), and WebGL2/WebGPU is used under the hood via luma.gl v9.
- If you don't need React, you can use `Deck` from `@deck.gl/core` instead of `<DeckGL>`, and drop the react-map-gl dependencies entirely — deck.gl v9 supports `MapboxOverlay` or standalone canvas mode.
- If avoiding Mapbox entirely, `<DeckGL>` renders fine with a dark background and no basemap.