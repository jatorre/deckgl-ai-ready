<!-- model: claude-fable-5-1 | prompt: P7_deckgl_json_spec | seconds: 26 | backend: claude-cli tools=none -->
```json
{
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "views": [
    {
      "@@type": "MapView",
      "controller": true
    }
  ],
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries-by-population",
      "data": "https://example.com/countries.geojson",
      "pickable": true,
      "stroked": true,
      "filled": true,
      "opacity": 0.8,
      "lineWidthMinPixels": 1,
      "getLineColor": [90, 90, 90, 200],
      "getFillColor": "@@=properties.population > 100000000 ? [127, 0, 0, 220] : properties.population > 50000000 ? [215, 48, 31, 220] : properties.population > 20000000 ? [239, 101, 72, 220] : properties.population > 5000000 ? [252, 141, 89, 220] : properties.population > 1000000 ? [253, 204, 138, 220] : [254, 240, 217, 220]"
    }
  ]
}
```
