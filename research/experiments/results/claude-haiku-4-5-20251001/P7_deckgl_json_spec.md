<!-- model: claude-haiku-4-5-20251001 | prompt: P7_deckgl_json_spec | seconds: 15 | backend: claude-cli tools=none -->
```json
{
  "version": "8.8",
  "config": {
    "mapStyle": "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json",
    "initialViewState": {
      "latitude": 54.5,
      "longitude": 15,
      "zoom": 4,
      "bearing": 0,
      "pitch": 0
    }
  },
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "data": "https://example.com/countries.geojson",
      "filled": true,
      "stroked": true,
      "getFillColor": {
        "@@type": "colorBinScale",
        "accessor": "properties.population",
        "domain": [0, 50000000, 100000000, 500000000, 1000000000, 1500000000],
        "range": [
          [255, 255, 178],
          [254, 204, 92],
          [253, 141, 60],
          [252, 78, 42],
          [227, 26, 28],
          [189, 0, 38]
        ]
      },
      "getLineColor": [200, 200, 200],
      "getLineWidth": 1,
      "pickable": true
    }
  ]
}
```
