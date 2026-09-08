<!-- model: claude-fable-5-1 | prompt: P3_h3_hexagons | seconds: 15 | backend: claude-cli tools=none -->
Use deck.gl's H3HexagonLayer over a MapLibre basemap. It renders H3 indexes natively, so you skip converting cells to polygons, and it stays smooth at hundreds of thousands of cells.

Recommended stack:

- **deck.gl** for rendering. The `H3HexagonLayer` in `@deck.gl/geo-layers` takes H3 indexes directly.
- **MapLibre GL JS** for the basemap. Free, open source, and deck.gl integrates with it through `MapboxOverlay`.
- **d3-scale** for the color ramp. Pick a sequential scheme and map count to color.

Install:

```bash
npm install deck.gl maplibre-gl d3-scale d3-scale-chromatic
```

Minimal example, assuming `data` is an array like `[{ h3: '8928308280fffff', count: 42 }]`:

```js
import maplibregl from 'maplibre-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { H3HexagonLayer } from '@deck.gl/geo-layers';
import { scaleSequential } from 'd3-scale';
import { interpolateViridis } from 'd3-scale-chromatic';
import { rgb } from 'd3-color';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  center: [-3.7038, 40.4168],
  zoom: 11
});

const maxCount = Math.max(...data.map(d => d.count));
const color = scaleSequential(interpolateViridis).domain([0, maxCount]);

const layer = new H3HexagonLayer({
  id: 'h3-counts',
  data,
  getHexagon: d => d.h3,
  getFillColor: d => {
    const c = rgb(color(d.count));
    return [c.r, c.g, c.b, 200];
  },
  extruded: false,
  pickable: true
});

map.addControl(new MapboxOverlay({
  layers: [layer],
  getTooltip: ({ object }) => object && `Count: ${object.count}`
}));
```

Two notes. Use a log or quantile scale instead of linear if counts are heavily skewed, otherwise most hexes look identical. If you are working inside CARTO, the `@deck.gl/carto` package can load H3 tables straight from the warehouse and handles tiling for you.
