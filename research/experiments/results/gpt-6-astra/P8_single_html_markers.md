<!-- model: openai/gpt-6-astra | prompt: P8_single_html_markers | seconds: 14 | backend: openrouter | usage: {"prompt_tokens": 51, "completion_tokens": 771, "total_tokens": 822, "cost": 0.03906, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03906, "upstream_inference_prompt_cost": 0.00051, "upstream_inference_completions_cost": 0.03855}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>European Cities Map</title>

  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""
  >

  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: system-ui, sans-serif;
      color: #172033;
      background: #f5f7fb;
    }

    header {
      padding: 18px 24px;
      background: #fff;
      border-bottom: 1px solid #dde3ec;
    }

    h1 {
      margin: 0 0 6px;
      font-size: 1.4rem;
    }

    p {
      margin: 0;
      color: #526176;
    }

    main {
      display: flex;
      flex-direction: column;
      height: 100vh;
      height: 100dvh;
    }

    #map {
      flex: 1;
      min-height: 300px;
    }

    .leaflet-popup-content {
      font-size: 16px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Explore European Cities</h1>
      <p>Select a marker to see its city name. Drag to pan and use the controls to zoom.</p>
    </header>
    <div id="map" role="region" aria-label="Interactive map of Madrid, Zurich, Berlin, Lisbon and Oslo"></div>
  </main>

  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
  ></script>

  <script>
    const cities = [
      { name: "Madrid", coordinates: [40.4168, -3.7038] },
      { name: "Zurich", coordinates: [47.3769, 8.5417] },
      { name: "Berlin", coordinates: [52.5200, 13.4050] },
      { name: "Lisbon", coordinates: [38.7223, -9.1393] },
      { name: "Oslo", coordinates: [59.9139, 10.7522] }
    ];

    const map = L.map("map");

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const markers = cities.map(city =>
      L.marker(city.coordinates, {
        title: city.name,
        alt: city.name,
        keyboard: true
      })
        .addTo(map)
        .bindPopup(city.name)
    );

    map.fitBounds(L.featureGroup(markers).getBounds(), {
      padding: [40, 40]
    });
  </script>
</body>
</html>