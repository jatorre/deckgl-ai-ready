<!-- model: openai/gpt-6-astra | prompt: P7_deckgl_json_spec | seconds: 10 | backend: openrouter | usage: {"prompt_tokens": 63, "completion_tokens": 415, "total_tokens": 478, "cost": 0.02138, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.02138, "upstream_inference_prompt_cost": 0.00063, "upstream_inference_completions_cost": 0.02075}, "completion_tokens_details": {"reasoning_tokens": 110, "image_tokens": 0, "audio_tokens": 0}} -->
{
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "controller": true,
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries-by-population",
      "data": "https://example.com/countries.geojson",
      "filled": true,
      "stroked": true,
      "pickable": true,
      "opacity": 0.8,
      "getFillColor": "@@=properties.population == null ? [200, 200, 200] : properties.population >= 100000000 ? [8, 48, 107] : properties.population >= 50000000 ? [8, 81, 156] : properties.population >= 10000000 ? [33, 113, 181] : properties.population >= 1000000 ? [107, 174, 214] : [198, 219, 239]",
      "getLineColor": [255, 255, 255],
      "getLineWidth": 1,
      "lineWidthUnits": "pixels",
      "lineWidthMinPixels": 1
    }
  ]
}