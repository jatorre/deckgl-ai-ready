<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P8_single_html_markers | seconds: 14 | backend: litellm-proxy | usage: {"completion_tokens": 1274, "prompt_tokens": 51, "total_tokens": 1325, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 448, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Interactive Map — Madrid, Zurich, Berlin, Lisbon, Oslo</title>

  <!-- Leaflet CSS -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-sA+e2q4p8bQY/6C2e3Yk3bq8dQ6Yqjv0z0q8q2mZ5+s="
    crossorigin=""
  />

  <style>
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
    }
    #map {
      height: 100vh; /* full viewport height */
      width: 100%;
    }
    /* small attribution/credit tweak so it doesn't overlap on small screens */
    .leaflet-control-attribution { font-size: 12px; }
  </style>
</head>
<body>
  <div id="map" aria-label="Map showing Madrid, Zurich, Berlin, Lisbon and Oslo"></div>

  <!-- Leaflet JS -->
  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-o9N1j7kR1b6Q0n0+5nq6gk3qz3b9p5u8n2XoT2v9mGk="
    crossorigin=""
  ></script>

  <script>
    // Create the map
    const map = L.map('map', {
      zoomControl: true,
      attributionControl: true
    });

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Cities with coordinates
    const cities = [
      { name: 'Madrid',   coords: [40.4168, -3.7038] },
      { name: 'Zurich',   coords: [47.3769,  8.5417] },
      { name: 'Berlin',   coords: [52.5200, 13.4050] },
      { name: 'Lisbon',   coords: [38.7223, -9.1393] },
      { name: 'Oslo',     coords: [59.9139, 10.7522] }
    ];

    // Add markers and popups
    const markers = [];
    cities.forEach(city => {
      const marker = L.marker(city.coords).addTo(map)
        .bindPopup('<strong>' + city.name + '</strong>');
      markers.push(marker);
    });

    // Fit map to markers
    const group = L.featureGroup(markers);
    map.fitBounds(group.getBounds().pad(0.15));

    // Optional: open popup when marker clicked is default behavior.
    // For accessibility: allow focusing markers with keyboard (tabindex)
    // Add keyboard support: open popup on Enter/Space when focused
    markers.forEach(marker => {
      const el = marker.getElement && marker.getElement();
      if (el) {
        el.setAttribute('tabindex', '0');
        el.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            marker.openPopup();
            e.preventDefault();
          }
        });
      }
    });
  </script>
</body>
</html>