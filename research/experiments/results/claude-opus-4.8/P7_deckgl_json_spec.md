<!-- model: anthropic/claude-opus-4.8 | prompt: P7_deckgl_json_spec | seconds: 10 | backend: openrouter | usage: {"prompt_tokens": 95, "completion_tokens": 790, "total_tokens": 885, "cost": 0.020225, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.020225, "upstream_inference_prompt_cost": 0.000475, "upstream_inference_completions_cost": 0.01975}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
```json
{
  "initialViewState": {
    "longitude": 10,
    "latitude": 50,
    "zoom": 4,
    "pitch": 0,
    "bearing": 0
  },
  "controller": true,
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
      "id": "countries",
      "data": "https://example.com/countries.geojson",
      "stroked": true,
      "filled": true,
      "pickable": true,
      "getLineColor": [255, 255, 255],
      "lineWidthMinPixels": 1,
      "getFillColor": {
        "@@function": "interpolateColor",
        "value": "@@=properties.population",
        "domain": [0, 10000000, 50000000, 100000000, 500000000, 1400000000],
        "colors": [
          [255, 245, 240],
          [252, 187, 161],
          [252, 146, 114],
          [251, 106, 74],
          [222, 45, 38],
          [165, 15, 21]
        ]
      }
    }
  ]
}
```

**Note:** The standard `@deck.gl/json` parser does not include a built-in `interpolateColor` function or a color-scale accessor. To make the `getFillColor` above work, you must register a custom function when constructing the `JSONConverter`, for example:

```js
import { JSONConverter } from '@deck.gl/json';
import { scaleThreshold } from 'd3-scale';

const configuration = {
  layers: { /* deck.gl layers */ },
  functions: {
    interpolateColor: ({ value, domain, colors }) => {
      const scale = scaleThreshold().domain(domain.slice(1)).range(colors);
      return d => scale(eval(value.replace('@@=', 'd.'))); // simplified
    }
  }
};

const converter = new JSONConverter({ configuration });
```

If you want a spec that works with **no custom functions**, replace `getFillColor` with a static/pre-computed field, or precompute a `fillColor` property per feature in the GeoJSON and use `"getFillColor": "@@=properties.fillColor"`.