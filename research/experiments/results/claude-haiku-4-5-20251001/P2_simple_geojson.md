<!-- model: claude-haiku-4-5-20251001 | prompt: P2_simple_geojson | seconds: 9 | backend: claude-cli tools=none -->
**Use Leaflet.js** — it's lightweight, easy to learn, and perfect for this use case. Mapbox GL would be overkill unless you need advanced styling or massive datasets.

Here's a minimal example:

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
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map);
    
    fetch('airports.geojson')
      .then(res => res.json())
      .then(data => {
        L.geoJSON(data, {
          pointToLayer: (feature, latlng) => {
            const marker = L.circleMarker(latlng, { radius: 5, color: 'blue' });
            
            marker.bindTooltip(feature.properties.name || 'Airport', {
              permanent: false,
              direction: 'top'
            });
            
            return marker;
          }
        }).addTo(map);
      });
  </script>
</body>
</html>
```

**Why Leaflet:**
- Minimal setup (just two CDN links)
- Built-in GeoJSON support
- `.bindTooltip()` handles hover tooltips easily
- Excellent browser compatibility
- Active community

Just swap `airports.geojson` with your file path and adjust the `name` property to match your GeoJSON field. You can style circles with `circleMarker()` options like `fillColor`, `weight`, etc.
