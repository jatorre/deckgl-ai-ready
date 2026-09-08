<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P7_deckgl_json_spec | seconds: 9 | backend: litellm-proxy | usage: {"completion_tokens": 1549, "prompt_tokens": 59, "total_tokens": 1608, "completion_tokens_details": {"reasoning_tokens": 1147, "text_tokens": 402}, "prompt_tokens_details": {"text_tokens": 59}} -->
{
  "initialViewState": {
    "longitude": 15.0,
    "latitude": 50.0,
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
      "id": "countries-geojson",
      "data": "https://example.com/countries.geojson",
      "filled": true,
      "stroked": true,
      "lineWidthMinPixels": 1,
      "getLineColor": [255, 255, 255, 180],
      "getFillColor": "@@=properties.population > 80000000 ? [189, 0, 38, 200] : properties.population > 40000000 ? [240, 59, 32, 200] : properties.population > 20000000 ? [253, 141, 60, 200] : properties.population > 10000000 ? [254, 204, 92, 200] : [255, 255, 178, 200]",
      "pickable": true,
      "autoHighlight": true
    }
  ]
}