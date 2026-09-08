<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P7_deckgl_json_spec | seconds: 17 | backend: litellm-proxy max_tokens=12000 | usage: {"completion_tokens": 2291, "prompt_tokens": 59, "total_tokens": 2350, "completion_tokens_details": {"reasoning_tokens": 1939, "text_tokens": 352}, "prompt_tokens_details": {"text_tokens": 59}} -->
{
  "initialViewState": {
    "longitude": 15.0,
    "latitude": 50.0,
    "zoom": 4
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
      "id": "countries-population-layer",
      "data": "https://example.com/countries.geojson",
      "pickable": true,
      "stroked": true,
      "filled": true,
      "lineWidthMinPixels": 1,
      "getLineColor": [200, 200, 200],
      "getFillColor": "@@=properties.population > 100000000 ? [189, 0, 38] : properties.population > 50000000 ? [240, 59, 32] : properties.population > 20000000 ? [253, 141, 60] : properties.population > 10000000 ? [254, 204, 92] : [255, 255, 178]"
    }
  ]
}