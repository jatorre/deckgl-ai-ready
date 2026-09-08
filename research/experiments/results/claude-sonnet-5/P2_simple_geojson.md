<!-- model: claude-sonnet-5 | prompt: P2_simple_geojson | seconds: 8 | backend: claude-cli tools=none -->
For a simple point map with hover tooltips, **Leaflet** is the best fit — lightweight, no build step needed, and has built-in tooltip support.

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
  <style>
    #map { height: 100vh; margin: 0; }
    body { margin: 0; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
  <script>
    const map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetch('airports.geojson')
      .then(res => res.json())
      .then(data => {
        L.geoJSON(data, {
          pointToLayer: (feature, latlng) =>
            L.circleMarker(latlng, {
              radius: 4,
              fillColor: '#ff5722',
              color: '#fff',
              weight: 1,
              fillOpacity: 0.8
            }),
          onEachFeature: (feature, layer) => {
            layer.bindTooltip(feature.properties.name, {
              direction: 'top',
              offset: [0, -4]
            });
          }
        }).addTo(map);
      });
  </script>
</body>
</html>
```

Notes:
- Assumes `airports.geojson` has Point features with a `properties.name` field. Adjust the property key if your data uses something like `airport_name` or `NAME`.
- `L.circleMarker` performs well for a few thousand points; if you have tens of thousands of airports, consider `Leaflet.markercluster` or switch to `deck.gl`/MapLibre GL for GPU-accelerated rendering.
- Serve the files via a local HTTP server (e.g. `npx serve`) since `fetch` on a local GeoJSON file won't work with `file://` URLs in most browsers.
