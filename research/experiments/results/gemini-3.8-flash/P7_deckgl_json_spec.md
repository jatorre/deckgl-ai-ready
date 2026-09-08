<!-- model: google/gemini-3.8-flash | prompt: P7_deckgl_json_spec | seconds: 19 | backend: openrouter | usage: {"prompt_tokens": 59, "completion_tokens": 2755, "total_tokens": 2814, "cost": 0.0103755, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0103755, "upstream_inference_prompt_cost": 4.425e-05, "upstream_inference_completions_cost": 0.01033125}, "completion_tokens_details": {"reasoning_tokens": 2353, "image_tokens": 0, "audio_tokens": 0}} -->
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
      "id": "countries-population",
      "data": "https://example.com/countries.geojson",
      "filled": true,
      "stroked": true,
      "lineWidthUnits": "pixels",
      "getLineWidth": 1,
      "getLineColor": [255, 255, 255, 180],
      "getFillColor": "@@=properties.population > 80000000 ? [189, 0, 38, 200] : properties.population > 40000000 ? [240, 59, 32, 200] : properties.population > 20000000 ? [253, 141, 60, 200] : properties.population > 10000000 ? [254, 204, 92, 200] : [255, 255, 178, 200]",
      "pickable": true
    }
  ]
}