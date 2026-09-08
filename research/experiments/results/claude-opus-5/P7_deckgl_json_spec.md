<!-- model: claude-opus-5 | prompt: P7_deckgl_json_spec | seconds: 16 | backend: claude-cli tools=none -->
```json
{
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "views": [
    {
      "@@type": "MapView",
      "controller": true
    }
  ],
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries-population",
      "data": "https://example.com/countries.geojson",
      "stroked": true,
      "filled": true,
      "extruded": false,
      "pickable": true,
      "autoHighlight": true,
      "highlightColor": [255, 255, 255, 80],
      "getFillColor": "@@=properties.population > 100000000 ? [128, 0, 38, 200] : properties.population > 50000000 ? [189, 0, 38, 200] : properties.population > 20000000 ? [227, 26, 28, 200] : properties.population > 10000000 ? [252, 78, 42, 200] : properties.population > 5000000 ? [253, 141, 60, 200] : properties.population > 1000000 ? [254, 178, 76, 200] : properties.population > 0 ? [254, 217, 118, 200] : [220, 220, 220, 120]",
      "getLineColor": [255, 255, 255, 180],
      "getLineWidth": 1,
      "lineWidthUnits": "pixels",
      "lineWidthMinPixels": 0.5,
      "updateTriggers": {
        "getFillColor": ["population"]
      }
    }
  ]
}
```
