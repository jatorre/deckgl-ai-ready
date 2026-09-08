<!-- model: claude-opus-5 | prompt: P8_single_html_markers | seconds: 18 | backend: claude-cli tools=none -->
I'll use Leaflet — no API key, no build step, single CDN include. Basemap tiles from CARTO's Voyager style.


<invoke name="Write">
<parameter name="path">/private/tmp/claude-502/-Users-jatorre-workspace-openvis-summit-2026/0fcc559d-5a16-4e20-8d22-d6dafbba654f/scratchpad/exp-cwd/map.html</parameter>
<parameter name="content"><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>European Cities</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body { margin: 0; padding: 0; height: 100%; }
    #map { height: 100%; width: 100%; background: #f2efe9; }
    .leaflet-popup-content { font: 600 14px/1.3 system-ui, -apple-system, "Segoe UI", sans-serif; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const cities = [
      { name: 'Madrid', coords: [40.4168, -3.7038] },
      { name: 'Zurich', coords: [47.3769,  8.5417] },
      { name: 'Berlin', coords: [52.5200, 13.4050] },
      { name: 'Lisbon', coords: [38.7223, -9.1393] },
      { name: 'Oslo',   coords: [59.9139, 10.7522] }
    ];

    const map = L.map('map');

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd',
      maxZoom: 20,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }).addTo(map);

    const markers = cities.map(city =>
      L.marker(city.coords)
        .addTo(map)
        .bindPopup(city.name)
    );

    // Frame all five cities regardless of window size.
    map.fitBounds(L.featureGroup(markers).getBounds(), { padding: [50, 50] });
  </script>
</body>
</html>
</parameter>
</invoke>

<invoke name="Bash">
<parameter name="command">cd /private/tmp/claude-502/-Users-jatorre-workspace-openvis-summit-2026/0fcc559d-5a16-4e20-8d22-d6dafbba654f/scratchpad/exp-cwd && wc -c map.html && open map.html</parameter>
<parameter name="description">Check size and open map in browser</parameter>
</invoke>


    1732 bytes map.html
