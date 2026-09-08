<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P7_deckgl_json_spec | seconds: 6 | backend: litellm-proxy | usage: {"completion_tokens": 413, "prompt_tokens": 63, "total_tokens": 476, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
{
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "bearing": 0,
    "pitch": 0
  },
  "views": [
    {
      "@@type": "MapView",
      "id": "map"
    }
  ],
  "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "controller": true,
  "layers": [
    {
      "@@type": "GeoJsonLayer",
      "id": "countries",
      "data": "https://example.com/countries.geojson",
      "pickable": true,
      "stroked": true,
      "filled": true,
      "lineWidthMinPixels": 0.5,
      "getLineColor": [
        255,
        255,
        255,
        180
      ],
      "getLineWidth": 1,
      "getFillColor": {
        "@@type": "Expression",
        "expression": [
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
            247,
            251,
            255,
            220
          ],
          1000000,
          [
            198,
            219,
            239,
            220
          ],
          10000000,
          [
            107,
            174,
            214,
            220
          ],
          50000000,
          [
            33,
            113,
            181,
            220
          ],
          200000000,
          [
            8,
            48,
            107,
            220
          ]
        ]
      },
      "updateTriggers": {
        "getFillColor": [
          "population"
        ]
      }
    }
  ]
}