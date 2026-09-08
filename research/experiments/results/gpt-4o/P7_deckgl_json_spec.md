<!-- model: ac_7xhfwyml::openai::gpt-4o | prompt: P7_deckgl_json_spec | seconds: 3 | backend: litellm-proxy | usage: {"completion_tokens": 244, "prompt_tokens": 64, "total_tokens": 308, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
```json
{
  "initialViewState": {
    "latitude": 54.526,
    "longitude": 15.2551,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "controller": true,
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "geojson-layer",
      "data": "https://example.com/countries.geojson",
      "opacity": 0.8,
      "stroked": false,
      "filled": true,
      "extruded": false,
      "getFillColor": [
        "get",
        "population",
        [
          [0, 255, 255],
          [0, 255, 0],
          [255, 255, 0],
          [255, 0, 0]
        ]
      ],
      "getLineColor": [255, 255, 255],
      "getLineWidth": 1
    }
  ],
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
}
```