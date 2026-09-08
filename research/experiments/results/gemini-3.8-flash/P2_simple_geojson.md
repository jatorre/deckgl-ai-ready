<!-- model: google/gemini-3.8-flash | prompt: P2_simple_geojson | seconds: 8 | backend: openrouter | usage: {"prompt_tokens": 47, "completion_tokens": 1302, "total_tokens": 1349, "cost": 0.00491775, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.00491775, "upstream_inference_prompt_cost": 3.525e-05, "upstream_inference_completions_cost": 0.0048825}, "completion_tokens_details": {"reasoning_tokens": 744, "image_tokens": 0, "audio_tokens": 0}} -->
Use **Leaflet.js**. It is free, lightweight, requires no API key, and natively handles GeoJSON with built-in tooltip support.

### Minimal HTML/JS Example

Save this as `index.html` and place your `airports.geojson` file in the same directory (ensure it is served via a local web server to avoid CORS issues).

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>World Airports Map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    body { margin: 0; }
    #map { height: 100vh; width: 100vw; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    // Initialize the map centered globally
    const map = L.map('map').setView([20, 0], 2);

    // Add free OpenStreetMap base tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Fetch and display GeoJSON
    fetch('airports.geojson')
      .then(response => response.json())
      .then(data => {
        L.geoJSON(data, {
          // Render points as small circle markers for better performance
          pointToLayer: (feature, latlng) => L.circleMarker(latlng, {
            radius: 4,
            fillColor: "#0078ff",
            color: "#000",
            weight: 1,
            fillOpacity: 0.8
          }),
          // Attach hover tooltip
          onEachFeature: (feature, layer) => {
            if (feature.properties && feature.properties.name) {
              layer.bindTooltip(feature.properties.name);
            }
          }
        }).addTo(map);
      });
  </script>
</body>
</html>
```

*Note: Replace `feature.properties.name` with the exact property key containing the airport name in your GeoJSON file (e.g., `NAME` or `airport_name`).*