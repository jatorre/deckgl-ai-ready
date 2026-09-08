<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P3_h3_hexagons | seconds: 15 | backend: litellm-proxy | usage: {"completion_tokens": 1583, "prompt_tokens": 59, "total_tokens": 1642, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 832, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Libraries I recommend
- deck.gl (built-in H3HexagonLayer, high-performance, WebGL).
- mapbox-gl or maplibre-gl (basemap under deck.gl).
- h3-js + Leaflet (if you prefer simpler 2D vector polygons).
- kepler.gl (no-code/GUI exploration).

Minimal example (deck.gl + Mapbox): paste into an HTML file, set MAPBOX_TOKEN.

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>H3 hex map — deck.gl</title>
  <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
  <link href="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css" rel="stylesheet" />
  <script src="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.0/dist.min.js"></script>
</head>
<body>
<div id="map" style="position:absolute;inset:0"></div>
<script>
const MAPBOX_TOKEN = 'YOUR_MAPBOX_TOKEN';

// sample H3-aggregated data: {h3: '8928308280fffff', value: 10}
const data = [
  {h3: '8928308280fffff', value: 5},
  {h3: '8928308281fffff', value: 20},
  {h3: '8928308283fffff', value: 50}
];

// simple linear color scale from blue (low) to red (high)
const values = data.map(d=>d.value);
const min = Math.min(...values), max = Math.max(...values);
const colorFor = v => {
  const t = (v - min) / Math.max(1e-6, max - min);
  const r = Math.round(255 * t), g = 50, b = Math.round(255 * (1-t));
  return [r,g,b,180];
};

const map = new mapboxgl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4, 37.76],
  zoom: 11,
  interactive: true
});

map.on('load', () => {
  const deckgl = new deck.DeckGL({
    canvas: 'deck-canvas',
    width: '100%',
    height: '100%',
    initialViewState: {
      longitude: -122.4, latitude: 37.76, zoom: 11
    },
    controller: true,
    layers: [
      new deck.H3HexagonLayer({
        id: 'h3-layer',
        data,
        getHexagon: d => d.h3,
        getFillColor: d => colorFor(d.value),
        pickable: true,
        extruded: false,
        opacity: 0.9
      })
    ]
  });
  // make deck use the map's container
  map.getCanvas().style.position = 'absolute';
  map.getCanvas().id = 'deck-canvas';
});
</script>
</body>
</html>
```

Notes: For Leaflet use h3-js.h3ToGeoBoundary to create GeoJSON polygons and color-by-value. Deck.gl's H3HexagonLayer is simplest if you already have H3 indexes.