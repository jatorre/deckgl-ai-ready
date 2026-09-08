<!-- model: anthropic/claude-opus-4.8 | prompt: P2_simple_geojson | seconds: 11 | backend: openrouter | usage: {"prompt_tokens": 77, "completion_tokens": 915, "total_tokens": 992, "cost": 0.02326, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.02326, "upstream_inference_prompt_cost": 0.000385, "upstream_inference_completions_cost": 0.022875}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Interactive Airport Map

**Recommended library: [Leaflet](https://leafletjs.com/)**

Leaflet is lightweight, free, easy to learn, and perfect for point data like airports with tooltips. (Alternatives: MapLibre GL JS for vector/3D, but Leaflet is simplest here.)

## Minimal Example

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>World Airports</title>
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    #map { height: 100vh; width: 100%; margin: 0; }
    body { margin: 0; }
  </style>
</head>
<body>
  <div id="map"></div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    // Initialize map
    const map = L.map('map').setView([20, 0], 2);

    // Add base tiles (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Load GeoJSON airports
    fetch('airports.geojson')
      .then(res => res.json())
      .then(data => {
        L.geoJSON(data, {
          // Render each point as a small circle marker
          pointToLayer: (feature, latlng) =>
            L.circleMarker(latlng, { radius: 4, color: '#e63946' }),
          // Bind hover tooltip with airport name
          onEachFeature: (feature, layer) => {
            const name = feature.properties.name || 'Unknown Airport';
            layer.bindTooltip(name); // shows on hover by default
          }
        }).addTo(map);
      });
  </script>
</body>
</html>
```

## Notes
- **GeoJSON format**: expects `Point` features with coordinates `[lon, lat]` and a `properties.name` field. Adjust the property key to match your file.
- **Tooltips** display on hover automatically for `bindTooltip`. Use `.bindPopup()` if you prefer click-to-open.
- **Performance tip**: for thousands of airports, add [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) to group markers.

Serve the file via a local server (e.g. `python -m http.server`) so `fetch` can load the GeoJSON.