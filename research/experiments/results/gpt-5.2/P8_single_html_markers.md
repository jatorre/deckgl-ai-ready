<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P8_single_html_markers | seconds: 7 | backend: litellm-proxy | usage: {"completion_tokens": 621, "prompt_tokens": 51, "total_tokens": 672, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>European Cities Map</title>

  <!-- Leaflet CSS -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""
  />

  <style>
    html, body { height: 100%; margin: 0; }
    #map { height: 100%; width: 100%; }
  </style>
</head>
<body>
  <div id="map" aria-label="Interactive map of European cities"></div>

  <!-- Leaflet JS -->
  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
  ></script>

  <script>
    // Initialize map (centered roughly over Western/Central Europe)
    const map = L.map('map', { scrollWheelZoom: true }).setView([50.5, 10.0], 4);

    // Base layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // City coordinates
    const cities = [
      { name: 'Madrid',  lat: 40.4168, lng: -3.7038 },
      { name: 'Zurich',  lat: 47.3769, lng:  8.5417 },
      { name: 'Berlin',  lat: 52.5200, lng: 13.4050 },
      { name: 'Lisbon',  lat: 38.7223, lng: -9.1393 },
      { name: 'Oslo',    lat: 59.9139, lng: 10.7522 }
    ];

    const bounds = L.latLngBounds();

    cities.forEach(c => {
      const marker = L.marker([c.lat, c.lng]).addTo(map);
      marker.bindPopup(`<strong>${c.name}</strong>`);
      bounds.extend([c.lat, c.lng]);
    });

    // Fit map to show all markers nicely
    map.fitBounds(bounds.pad(0.2));
  </script>
</body>
</html>
```