<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P2_simple_geojson | seconds: 6 | backend: litellm-proxy | usage: {"completion_tokens": 437, "prompt_tokens": 52, "total_tokens": 489, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Use **Leaflet**. It’s lightweight, easy to set up, works great with GeoJSON, and supports hover tooltips out of the box.

Minimal example (points GeoJSON with a `name` property):

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>World Airports</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>#map{height:100vh;margin:0}</style>
</head>
<body>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  // 1) Create map + basemap
  const map = L.map('map').setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // 2) Load your GeoJSON (airports.geojson)
  fetch('airports.geojson')
    .then(r => r.json())
    .then(geojson => {
      L.geoJSON(geojson, {
        pointToLayer: (feature, latlng) =>
          L.circleMarker(latlng, { radius: 4, color: '#1976d2', weight: 1, fillOpacity: 0.8 }),
        onEachFeature: (feature, layer) => {
          const name = feature.properties?.name ?? 'Unnamed airport';
          layer.bindTooltip(name, { direction: 'top', sticky: true }); // hover tooltip
        }
      }).addTo(map);
    });
</script>
</body>
</html>
```

Put `airports.geojson` next to the HTML file and serve via a local web server (e.g., `python -m http.server`) so `fetch()` works.