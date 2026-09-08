<!-- model: anthropic/claude-opus-4.8 | prompt: P1_large_points | seconds: 11 | backend: openrouter | usage: {"prompt_tokens": 103, "completion_tokens": 873, "total_tokens": 976, "cost": 0.02234, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.02234, "upstream_inference_prompt_cost": 0.000515, "upstream_inference_completions_cost": 0.021825}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Recommended Stack: deck.gl + MapLibre GL JS

For 2 million points with smooth pan/zoom, use **deck.gl** (GPU-accelerated WebGL rendering) layered over **MapLibre GL JS** (free, open-source basemap). deck.gl handles millions of points effortlessly because rendering happens on the GPU, not the DOM.

## Why this stack
- **deck.gl `ScatterplotLayer`** renders millions of points in a single GPU draw call
- **MapLibre** provides the interactive vector basemap (no Mapbox token needed)
- They integrate cleanly via `MapboxOverlay`

## Minimal Example

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet"/>
  <script src="https://unpkg.com/deck.gl@9/dist.min.js"></script>
  <style>#map{position:absolute;width:100%;height:100%}</style>
</head>
<body>
  <div id="map"></div>
  <script>
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [-122.4, 37.77], zoom: 10
    });

    // data: [{position:[lng,lat], speed:number}, ...] — load ~2M points
    fetch('points.json').then(r => r.json()).then(data => {
      const overlay = new deck.MapboxOverlay({
        layers: [
          new deck.ScatterplotLayer({
            id: 'gps',
            data,
            getPosition: d => d.position,
            getFillColor: d => {
              const t = Math.min(d.speed / 120, 1); // 0–120 km/h
              return [t * 255, 0, (1 - t) * 255]; // blue→red
            },
            radiusMinPixels: 1.5,
            getRadius: 2
          })
        ]
      });
      map.addControl(overlay);
    });
  </script>
</body>
</html>
```

## Performance Tips
- Serve data as **binary** (typed arrays) or tiled with `MVTLayer` for faster loads
- Use `radiusUnits: 'pixels'` to avoid recomputation
- Consider **GPU aggregation** if you later need density heatmaps

This comfortably handles 2M+ points at 60fps.