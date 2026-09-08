<!-- model: claude-sonnet-5 | prompt: P8_single_html_markers | seconds: 8 | backend: claude-cli tools=none -->
I'll create a single-file HTML page using Leaflet (lightweight, no build step, loads from CDN) with markers and popups for the five cities.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>European Cities Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
  html, body { height: 100%; margin: 0; padding: 0; }
  #map { height: 100%; width: 100%; }
</style>
</head>
<body>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  const cities = [
    { name: "Madrid", lat: 40.4168, lng: -3.7038 },
    { name: "Zurich", lat: 47.3769, lng: 8.5417 },
    { name: "Berlin", lat: 52.5200, lng: 13.4050 },
    { name: "Lisbon", lat: 38.7223, lng: -9.1393 },
    { name: "Oslo",   lat: 59.9139, lng: 10.7522 }
  ];

  const map = L.map('map').setView([50, 5], 4);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  const markers = cities.map(city =>
    L.marker([city.lat, city.lng]).addTo(map).bindPopup(city.name)
  );

  const group = L.featureGroup(markers);
  map.fitBounds(group.getBounds().pad(0.3));
</script>
</body>
</html>
```

Save this as an `.html` file and open it in a browser. It uses Leaflet + OpenStreetMap tiles from CDNs, so an internet connection is required; the map auto-fits to show all five markers, and clicking any marker shows a popup with the city name.
