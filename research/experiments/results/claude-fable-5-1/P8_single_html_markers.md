<!-- model: claude-fable-5-1 | prompt: P8_single_html_markers | seconds: 25 | backend: claude-cli tools=none (rerun after hang) -->
I'll write a self-contained page using Leaflet loaded from a CDN, with OpenStreetMap tiles.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>European Cities Map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
  <style>
    html, body { margin: 0; padding: 0; height: 100%; }
    #map { width: 100%; height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    const cities = [
      { name: 'Madrid', lat: 40.4168, lng: -3.7038 },
      { name: 'Zurich', lat: 47.3769, lng: 8.5417 },
      { name: 'Berlin', lat: 52.5200, lng: 13.4050 },
      { name: 'Lisbon', lat: 38.7223, lng: -9.1393 },
      { name: 'Oslo',   lat: 59.9139, lng: 10.7522 }
    ];

    const map = L.map('map');

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const markers = cities.map(city =>
      L.marker([city.lat, city.lng]).addTo(map).bindPopup(`<strong>${city.name}</strong>`)
    );

    // Fit the view to show all five cities with some padding.
    map.fitBounds(L.featureGroup(markers).getBounds(), { padding: [40, 40] });
  </script>
</body>
</html>
```

Save this as an `.html` file and open it in a browser. Leaflet is loaded from unpkg and tiles come from OpenStreetMap, so it needs an internet connection but no build step or API key. Clicking any marker opens a popup with the city name, and the initial view is fitted to include all five cities.
