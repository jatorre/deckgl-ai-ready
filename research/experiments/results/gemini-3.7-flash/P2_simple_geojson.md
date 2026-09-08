<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P2_simple_geojson | seconds: 7 | backend: litellm-proxy | usage: {"completion_tokens": 1103, "prompt_tokens": 47, "total_tokens": 1150, "completion_tokens_details": {"reasoning_tokens": 558, "text_tokens": 545}, "prompt_tokens_details": {"text_tokens": 47}} -->
Use **Leaflet.js**. It is lightweight, beginner-friendly, and natively supports GeoJSON rendering and hover tooltips without requiring API keys.

### Minimal Code Example

Save this as an `.html` file and ensure your `airports.geojson` file is in the same directory (or replace the URL with a live GeoJSON link):

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
    // 1. Initialize the map
    const map = L.map('map').setView([20, 0], 2);

    // 2. Add base map tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 3. Fetch and display GeoJSON
    fetch('airports.geojson')
      .then(res => res.json())
      .then(data => {
        L.geoJSON(data, {
          pointToLayer: (feature, latlng) => {
            return L.circleMarker(latlng, {
              radius: 4,
              fillColor: "#ff7800",
              color: "#000",
              weight: 1,
              fillOpacity: 0.8
            });
          },
          onEachFeature: (feature, layer) => {
            // Bind hover tooltip (adjust property name if not 'name')
            const airportName = feature.properties.name || 'Unknown Airport';
            layer.bindTooltip(airportName, { sticky: true });
          }
        }).addTo(map);
      });
  </script>
</body>
</html>
```

*Note: The `{ sticky: true }` option ensures the tooltip follows the mouse cursor smoothly on hover.*