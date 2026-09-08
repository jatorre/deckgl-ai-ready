<!-- model: gpt-5.6-sol | prompt: P3_h3_hexagons | seconds: 31 | backend: codex-cli sandbox=read-only web_search=disabled -->
Recommended stack:

- **deck.gl** — `H3HexagonLayer` renders H3 cells directly and efficiently.
- **MapLibre GL JS** — open-source interactive basemap, no Mapbox dependency.
- **h3-js** — optional; convert coordinates, inspect resolutions, or find neighboring cells.
- **d3-scale** — optional color scales and legends.
- **Kepler.gl** — best for quick, low-code exploration rather than a custom application.

Minimal React example:

```bash
npm install deck.gl react-map-gl maplibre-gl
```

```jsx
import Map from "react-map-gl/maplibre";
import {DeckGL} from "@deck.gl/react";
import {H3HexagonLayer} from "@deck.gl/geo-layers";
import "maplibre-gl/dist/maplibre-gl.css";

const data = [
  {h3: "8928308280fffff", count: 12},
  {h3: "8928308280bffff", count: 47},
  {h3: "89283082873ffff", count: 90}
];

export default function App() {
  const max = Math.max(...data.map(d => d.count));

  const layer = new H3HexagonLayer({
    id: "counts",
    data,
    getHexagon: d => d.h3,
    getFillColor: d => {
      const t = d.count / max;
      return [255 * t, 70, 255 * (1 - t), 190];
    },
    getLineColor: [255, 255, 255],
    lineWidthMinPixels: 1,
    pickable: true,
    extruded: false
  });

  return (
    <DeckGL
      initialViewState={{
        longitude: -122.42,
        latitude: 37.77,
        zoom: 11
      }}
      controller
      layers={[layer]}
      getTooltip={({object}) =>
        object && `Count: ${object.count}`
      }
    >
      <Map mapStyle="https://demotiles.maplibre.org/style.json" />
    </DeckGL>
  );
}
```

For production, use a perceptually uniform scale such as Viridis, define fixed count thresholds, and aggregate cells to a consistent H3 resolution before rendering.