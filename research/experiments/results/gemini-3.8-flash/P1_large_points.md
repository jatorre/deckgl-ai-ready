<!-- model: google/gemini-3.8-flash | prompt: P1_large_points | seconds: 13 | backend: openrouter | usage: {"prompt_tokens": 66, "completion_tokens": 1790, "total_tokens": 1856, "cost": 0.006762, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.006762, "upstream_inference_prompt_cost": 4.95e-05, "upstream_inference_completions_cost": 0.0067125}, "completion_tokens_details": {"reasoning_tokens": 1068, "image_tokens": 0, "audio_tokens": 0}} -->
### Recommended Stack

* **Visualization:** **deck.gl** (`ScatterplotLayer`) + **MapLibre GL JS** (basemap).
* **Data Format:** **Flat typed arrays** (`Float32Array`) or **Apache Arrow**. 

**Why:** Rendering 2 million points at 60 FPS requires GPU instancing via WebGL/WebGPU. `deck.gl` handles this volume natively. **Crucial tip:** Do not load 2 million objects as GeoJSON/JSON; pass binary attributes directly to avoid massive JS memory overhead and garbage collection freezes.

---

### Minimal Example

Save and run as an `.html` file:

```html
<!DOCTYPE html>
<html>
<head>
  <style>body { margin: 0; }</style>
  <script src="https://unpkg.com/deck.gl@^9.0.0/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@^4.0.0/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@^4.0.0/dist/maplibre-gl.css" rel="stylesheet" />
</head>
<body>
<script>
  const N = 2_000_000;
  // Use typed arrays for memory efficiency
  const positions = new Float32Array(N * 2);
  const colors = new Uint8Array(N * 3);

  for (let i = 0; i < N; i++) {
    positions[i * 2] = -122.45 + (Math.random() - 0.5) * 0.4; // Longitude
    positions[i * 2 + 1] = 37.75 + (Math.random() - 0.5) * 0.4; // Latitude

    const speed = Math.random(); // Normalized speed 0-1
    colors[i * 3]     = speed * 255;       // R (red = fast)
    colors[i * 3 + 1] = 50;                // G
    colors[i * 3 + 2] = (1 - speed) * 255; // B (blue = slow)
  }

  new deck.DeckGL({
    mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initialViewState: { longitude: -122.45, latitude: 37.75, zoom: 11 },
    controller: true,
    layers: [
      new deck.ScatterplotLayer({
        id: 'gps-points',
        data: {
          length: N,
          attributes: {
            getPosition: { value: positions, size: 2 },
            getColor: { value: colors, size: 3 }
          }
        },
        radiusMinPixels: 1,
        radiusMaxPixels: 4,
        getPointRadius: 2
      })
    ]
  });
</script>
</body>
</html>
```