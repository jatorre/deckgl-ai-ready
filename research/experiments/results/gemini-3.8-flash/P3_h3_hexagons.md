<!-- model: google/gemini-3.8-flash | prompt: P3_h3_hexagons | seconds: 8 | backend: openrouter | usage: {"prompt_tokens": 53, "completion_tokens": 1117, "total_tokens": 1170, "cost": 0.0042285, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0042285, "upstream_inference_prompt_cost": 3.975e-05, "upstream_inference_completions_cost": 0.00418875}, "completion_tokens_details": {"reasoning_tokens": 425, "image_tokens": 0, "audio_tokens": 0}} -->
### Recommended Stack

*   **Deck.gl (`H3HexagonLayer`)**: The industry standard for H3. It renders H3 indices directly via WebGL/GPU without converting them to GeoJSON polygons first.
*   **MapLibre GL JS**: An open-source basemap provider to pair with Deck.gl.

---

### Minimal Example

Save this as an `.html` file and open it in any browser:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.css" rel="stylesheet" />
  <style>body { margin: 0; }</style>
</head>
<body>
<script>
  // Sample data: SF area H3 indices (resolution 8) with counts
  const data = [
    { hex: '8828308281fffff', count: 120 },
    { hex: '8828308283fffff', count: 85 },
    { hex: '8828308285fffff', count: 40 },
    { hex: '8828308287fffff', count: 200 }
  ];

  new deck.DeckGL({
    mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
    initialViewState: {
      longitude: -122.4194,
      latitude: 37.7749,
      zoom: 12,
      pitch: 30
    },
    controller: true,
    layers: [
      new deck.H3HexagonLayer({
        id: 'h3-layer',
        data,
        pickable: true,
        wireframe: false,
        filled: true,
        extruded: false,
        getHexagon: d => d.hex,
        // Color gradient: [R, G, B, Alpha] based on count
        getFillColor: d => [255, 255 - (d.count * 1.2), 0, 180],
        getTooltip: ({object}) => object && `Count: ${object.count}`
      })
    ]
  });
</script>
</body>
</html>
```

### Key Parameters:
* **`getHexagon`**: Points to the H3 index string.
* **`getFillColor`**: Maps the numeric `count` to an `[R, G, B, A]` color scale.
* **`extruded: true`** (Optional): Add `getElevation: d => d.count` to display 3D columns.