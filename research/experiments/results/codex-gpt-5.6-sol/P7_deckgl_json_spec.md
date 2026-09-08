<!-- model: gpt-5.6-sol | prompt: P7_deckgl_json_spec | seconds: 31 | backend: codex-cli sandbox=read-only web_search=disabled -->
{
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries",
      "data": "https://example.com/countries.geojson",
      "filled": true,
      "stroked": true,
      "getFillColor": {
        "@@function": "colorContinuous",
        "attr": "properties.population",
        "domain": [0, 10000000, 50000000, 100000000],
        "colors": [
          [255, 247, 236],
          [253, 174, 107],
          [230, 85, 13],
          [127, 39, 4]
        ]
      },
      "getLineColor": [255, 255, 255],
      "lineWidthMinPixels": 1,
      "pickable": true,
      "autoHighlight": true
    }
  ]
}