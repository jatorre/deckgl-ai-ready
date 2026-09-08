<!-- model: claude-haiku-4-5-20251001 | prompt: P1_large_points | seconds: 13 | backend: claude-cli tools=none -->
**Recommendation: Deck.gl with Mapbox GL (or MapLibre GL for open-source)**

Deck.gl is built for this exact problem—it uses WebGL to render millions of points smoothly. Pair it with Mapbox GL JS (or open-source MapLibre GL) as the base map, and you'll get interactive panning/zooming with color-coded points by speed.

**Why:** Deck.gl's WebGL rendering handles 2M points efficiently, has built-in ScatterplotLayer, and abstracts away GPU optimization. Mapbox GL provides the smooth tile-based basemap.

**Minimal example:**

```javascript
import mapboxgl from 'mapbox-gl';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

const data = gpsPoints; // Array of {longitude, lat, speed}

const layer = new ScatterplotLayer({
  data,
  getPosition: (d) => [d.longitude, d.lat],
  getRadius: 100,
  getColor: (d) => {
    const hue = (d.speed / maxSpeed) * 120; // Green to red
    return hslToRgb(hue, 100, 50);
  },
  radiusScale: 1,
  stroked: false,
  opacity: 0.8,
});

export default function Map() {
  const [viewState, setViewState] = useState({
    longitude: -74.0,
    latitude: 40.7,
    zoom: 12,
  });

  return (
    <DeckGL
      viewState={viewState}
      onViewStateChange={({ viewState }) => setViewState(viewState)}
      controller
      layers={[layer]}
      ContextProvider={MapContext.Provider}
    >
      <mapboxgl.StaticMap mapboxAccessToken={token} />
    </DeckGL>
  );
}
```

**Setup:** `npm install @deck.gl/react @deck.gl/layers mapbox-gl`

**Alternatives if budget is tight:** MapLibre GL + vector tiles (pre-aggregate/cluster data server-side) or Canvas-based clustering, but Deck.gl gives you the smoothest experience with minimal client-side engineering.
