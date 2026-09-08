<!-- model: z-ai/glm-5.3 | prompt: P5_deckgl_on_maplibre | seconds: 29 | backend: openrouter | usage: {"prompt_tokens": 53, "completion_tokens": 631, "total_tokens": 684, "cost": 0.0027005175, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0027005175, "upstream_inference_prompt_cost": 6.29375e-05, "upstream_inference_completions_cost": 0.00263758}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Deck.gl + MapLibre GL JS Integration

## Install packages

```bash
npm install deck.gl maplibre-gl
```

## How it works

MapLibre renders the base map; deck.gl overlays it using the `MapboxOverlay` interleave layer (works with MapLibre, its fork of Mapbox GL). Deck.gl layers draw on the same WebGL context, so they sync perfectly with pan/zoom.

## Complete example

```jsx
import Map from 'react-map-gl/maplibre'; // or use maplibre-gl directly
import 'maplibre-gl/dist/maplibre-gl.css';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

const INITIAL_VIEW = {
  longitude: -122.4,
  latitude: 37.8,
  zoom: 11,
  bearing: 0,
  pitch: 0
};

function App() {
  const [overlay] = useState(() =>
    new MapboxOverlay({
      layers: [
        new ScatterplotLayer({
          id: 'points',
          data: [
            { position: [-122.45, 37.8] },
            { position: [-122.38, 37.78] }
          ],
          getPosition: d => d.position,
          getRadius: 200,
          getFillColor: [255, 100, 0, 200]
        })
      ]
    })
  );

  return (
    <Map
      initialViewState={INITIAL_VIEW}
      mapStyle="https://demotiles.maplibre.org/style.json"
      style={{ width: '100vw', height: '100vh' }}
      onLoad={e => e.target.addControl(overlay)}
    />
  );
}
```

For a **vanilla JS** setup (no React), replace with:

```js
import maplibregl from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { ScatterplotLayer } from '@deck.gl/layers';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4, 37.8],
  zoom: 11
});

const deckOverlay = new MapboxOverlay({
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data: [{ position: [-122.45, 37.8] }, { position: [-122.38, 37.78] }],
      getPosition: d => d.position,
      getRadius: 200,
      getFillColor: [255, 100, 0, 200]
    })
  ]
});

map.addControl(deckOverlay);
```

Note: `@deck.gl/mapbox` is included as part of the `deck.gl` umbrella package — no separate install needed. For React, also run `npm install react-map-gl` and reference `react-map-gl/maplibre`.