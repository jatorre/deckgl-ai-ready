<!-- model: z-ai/glm-5.3 | prompt: P7_deckgl_json_spec | seconds: 5 | backend: openrouter | usage: {"prompt_tokens": 69, "completion_tokens": 317, "total_tokens": 386, "cost": 0.0014914, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0014914, "upstream_inference_prompt_cost": 9.66e-05, "upstream_inference_completions_cost": 0.0013948}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
{
  "initialViewState": {
    "longitude": 15,
    "latitude": 52,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "mapStyle": "https://basemaps.cartocdn.com/light_all/style.json",
  "views": [
    {
      "type": "MapView",
      "controller": true
    }
  ],
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries",
      "data": "https://example.com/countries.geojson",
      "stroked": true,
      "filled": true,
      "getFillColor": {
        "@@function": "quantileColorScale",
        "attr": "properties.population",
        "domain": [0, 10000000, 50000000, 100000000, 300000000],
        "colors": [
          [255, 247, 236, 200],
          [254, 232, 200, 200],
          [253, 212, 158, 200],
          [253, 187, 132, 200],
          [227, 74, 51, 200]
        ]
      },
      "getLineColor": [255, 255, 255],
      "lineWidthMinPixels": 1,
      "pickable": true,
      "opacity": 0.85
    }
  ]
}