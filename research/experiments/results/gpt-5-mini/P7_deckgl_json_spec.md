<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P7_deckgl_json_spec | seconds: 15 | backend: litellm-proxy | usage: {"completion_tokens": 1338, "prompt_tokens": 63, "total_tokens": 1401, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 960, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
{
  "views": [
    {
      "id": "map",
      "type": "MapView",
      "controller": true
    }
  ],
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "mapStyle": "mapbox://styles/mapbox/light-v10",
  "layers": [
    {
      "id": "countries-choropleth",
      "type": "GeoJsonLayer",
      "data": "https://example.com/countries.geojson",
      "pickable": true,
      "autoHighlight": true,
      "filled": true,
      "stroked": true,
      "lineWidthMinPixels": 1,
      "getLineColor": [
        200,
        200,
        200
      ],
      "getFillColor": [
        "interpolate",
        [
          "linear"
        ],
        [
          "get",
          "population"
        ],
        0,
        [
          255,
          255,
          204,
          220
        ],
        1000000,
        [
          255,
          237,
          160,
          220
        ],
        10000000,
        [
          254,
          178,
          76,
          220
        ],
        50000000,
        [
          253,
          141,
          60,
          220
        ],
        100000000,
        [
          240,
          59,
          32,
          220
        ]
      ],
      "opacity": 0.9
    }
  ]
}