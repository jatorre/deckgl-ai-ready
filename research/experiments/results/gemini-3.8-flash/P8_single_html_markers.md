<!-- model: google/gemini-3.8-flash | prompt: P8_single_html_markers | seconds: 18 | backend: openrouter | usage: {"prompt_tokens": 46, "completion_tokens": 2688, "total_tokens": 2734, "cost": 0.0101145, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0101145, "upstream_inference_prompt_cost": 3.45e-05, "upstream_inference_completions_cost": 0.01008}, "completion_tokens_details": {"reasoning_tokens": 1005, "image_tokens": 0, "audio_tokens": 0}} -->
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>European Cities Map</title>

  <!-- Leaflet CSS -->
  <link 
    rel="stylesheet" 
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" 
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" 
    crossorigin=""
  />

  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body, html {
      height: 100%;
      width: 100%;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    #map {
      height: 100vh;
      width: 100vw;
    }

    /* Floating control panel */
    .info-panel {
      position: absolute;
      top: 20px;
      left: 20px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 16px 20px;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
      max-width: 260px;
    }

    .info-panel h1 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 8px;
    }

    .info-panel p {
      font-size: 0.85rem;
      color: #64748b;
      margin-bottom: 12px;
    }

    .city-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .city-btn {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 0.78rem;
      font-weight: 500;
      color: #334155;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .city-btn:hover {
      background: #3b82f6;
      border-color: #3b82f6;
      color: #fff;
    }

    /* Popup customization */
    .custom-popup .leaflet-popup-content-wrapper {
      border-radius: 8px;
      padding: 4px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .custom-popup .leaflet-popup-content {
      margin: 8px 12px;
      font-size: 1rem;
      font-weight: 600;
      color: #0f172a;
      text-align: center;
    }
  </style>
</head>
<body>

  <!-- Floating UI Overlay -->
  <div class="info-panel">
    <h1>European Cities</h1>
    <p>Click a marker or select a city below to zoom in:</p>
    <div class="city-buttons" id="cityButtons"></div>
  </div>

  <!-- Map Container -->
  <div id="map"></div>

  <!-- Leaflet JS -->
  <script 
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" 
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" 
    crossorigin="">
  </script>

  <script>
    // City definitions: Name, Latitude, Longitude
    const cities = [
      { name: "Madrid",  coords: [40.4168, -3.7038] },
      { name: "Zurich",  coords: [47.3769, 8.5417] },
      { name: "Berlin",  coords: [52.5200, 13.4050] },
      { name: "Lisbon",  coords: [38.7223, -9.1393] },
      { name: "Oslo",    coords: [59.9139, 10.7522] }
    ];

    // Initialize map
    const map = L.map('map', {
      zoomControl: false // Moved/re-added later or styled cleanly
    });

    // Add Zoom control at bottom right for cleaner mobile UX
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Modern base map tiles (CartoDB Positron)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    const markersGroup = L.featureGroup();
    const buttonsContainer = document.getElementById('cityButtons');

    // Add markers and interactive buttons
    cities.forEach(city => {
      // 1. Create and bind marker
      const marker = L.marker(city.coords)
        .bindPopup(`<strong>${city.name}</strong>`, { className: 'custom-popup' });
      
      markersGroup.addLayer(marker);

      // 2. Create quick-jump button
      const button = document.createElement('button');
      button.className = 'city-btn';
      button.textContent = city.name;
      button.onclick = () => {
        map.flyTo(city.coords, 8, { duration: 1.2 });
        marker.openPopup();
      };
      buttonsContainer.appendChild(button);
    });

    // Add all markers to the map
    markersGroup.addTo(map);

    // Auto-fit the view to encompass all markers with nice padding
    map.fitBounds(markersGroup.getBounds(), {
      padding: [60, 60],
      maxZoom: 6
    });
  </script>
</body>
</html>
```