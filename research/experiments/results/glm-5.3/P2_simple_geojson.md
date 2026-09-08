<!-- model: z-ai/glm-5.3 | prompt: P2_simple_geojson | seconds: 8 | backend: openrouter | usage: {"prompt_tokens": 57, "completion_tokens": 472, "total_tokens": 529, "cost": 0.0021566, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0021566, "upstream_inference_prompt_cost": 7.98e-05, "upstream_inference_completions_cost": 0.0020768}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
## Recommended Library: **Leaflet**

Leaflet is the best choice here — it's lightweight (~42 KB), has no dependencies, and handles GeoJSON points natively with excellent tooltip support.

## Minimal Example

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    #map { height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    const map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    fetch('airports.geojson')
    {
      const data = await response.json();
      L.geoJSON(data, {
        onEachFeature: (feature, layer) => {
          layer.bindTooltip(feature.properties.name);
        }
      }).addTo(map);
    })();
  </script>
</body>
</html>
```

## Expected GeoJSON structure

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { "type": "Point", "coordinates": [-0.4543, 51.4700] },
      "properties": { "name": "Heathrow Airport" }
    }
  ]
}
```

## Key points

- **`bindTooltip()`** handles hover tooltips automatically — no mouse event code needed.
- GeoJSON coordinates are `[lon, lat]`, but Leaflet converts them to `[lat, lon]` for you.
- Serve the file over HTTP (e.g., `python -m http.server`) — `fetch` fails on `file://` URLs.

**Alternatives:** MapLibre GL JS if you want smooth vector/3D tilted maps, or OpenLayers for advanced projection needs. For a simple hover-tooltip use case, Leaflet wins on simplicity.