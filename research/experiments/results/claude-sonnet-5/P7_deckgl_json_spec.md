<!-- model: claude-sonnet-5 | prompt: P7_deckgl_json_spec | seconds: 5 | backend: claude-cli tools=none -->
```json
{
  "version": "1.0",
  "views": [
    {
      "@@type": "MapView",
      "controller": true
    }
  ],
  "initialViewState": {
    "longitude": 15,
    "latitude": 54,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries-layer",
      "data": "https://example.com/countries.geojson",
      "stroked": true,
      "filled": true,
      "extruded": false,
      "pickable": true,
      "getLineColor": [80, 80, 80],
      "lineWidthMinPixels": 1,
      "getFillColor": {
        "@@function": "colorContinuous",
        "attr": "population",
        "domain": [0, 1000000, 5000000, 20000000, 50000000, 100000000, 300000000],
        "colors": "Sunset",
        "nullColor": [204, 204, 204]
      }
    }
  ]
}
```
