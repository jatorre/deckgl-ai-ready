<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P1_large_points | seconds: 8 | backend: litellm-proxy | usage: {"completion_tokens": 1105, "prompt_tokens": 66, "total_tokens": 1171, "completion_tokens_details": {"reasoning_tokens": 403, "text_tokens": 702}, "prompt_tokens_details": {"text_tokens": 66}} -->
### Recommended Stack

* **Mapping & Visualization:** **deck.gl** overlaid on **MapLibre GL JS**. 
* **Data Handling:** Use binary buffers (**`Float32Array`** or Apache Arrow) instead of GeoJSON to bypass JSON-parsing bottlenecks for 2M points.

deck.gl utilizes WebGL to execute rendering directly on the GPU, effortlessly keeping 2M points at 60 FPS during pan/zoom.

---

### Minimal Implementation

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  <script src="https://unpkg.com/deck.gl@8.9.33/dist.min.js"></script>
  <style>body { margin: 0; }</style>
</head>
<body>
<script>
  // Generate 2M mock points: positions (lng, lat) and speeds (0-100 km/h)
  const count = 2000000;
  const positions = new Float32Array(count * 2);
  const colors = new Uint8Array(count * 3);

  for (let i = 0; i < count; i++) {
    positions[i * 2] = -122.4 + (Math.random() - 0.5) * 0.5; // Lng
    positions[i * 2 + 1] = 37.7 + (Math.random() - 0.5) * 0.5; // Lat
    
    // Color by speed: Blue (slow) to Red (fast)
    const speed = Math.random(); 
    colors[i * 3] = speed * 255;       // R
    colors[i * 3 + 1] = (1 - speed) * 100; // G
    colors[i * 3 + 2] = (1 - speed) * 255; // B
  }

  new deck.DeckGL({
    mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initialViewState: { longitude: -122.4, latitude: 37.7, zoom: 10 },
    controller: true,
    layers: [
      new deck.ScatterplotLayer({
        id: 'gps-points',
        data: {
          length: count,
          attributes: {
            getPosition: { value: positions, size: 2 },
            getFillColor: { value: colors, size: 3 }
          }
        },
        radiusMinPixels: 1,
        radiusMaxPixels: 5,
        getRadius: 10
      })
    ]
  });
</script>
</body>
</html>
```