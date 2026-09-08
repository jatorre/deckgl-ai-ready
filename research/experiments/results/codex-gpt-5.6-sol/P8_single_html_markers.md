<!-- model: gpt-5.6-sol | prompt: P8_single_html_markers | seconds: 23 | backend: codex-cli sandbox=read-only web_search=disabled -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>European Cities Map</title>

  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIINfQ3ynhZuuZs2OM2o1p1MZgqkLB6MZ6U="
    crossorigin=""
  >

  <style>
    html,
    body,
    #map {
      width: 100%;
      height: 100%;
      margin: 0;
    }
  </style>
</head>
<body>
  <div id="map" aria-label="Interactive map of European cities"></div>

  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
  ></script>

  <script>
    const map = L.map("map");

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const cities = [
      { name: "Madrid", coordinates: [40.4168, -3.7038] },
      { name: "Zurich", coordinates: [47.3769, 8.5417] },
      { name: "Berlin", coordinates: [52.5200, 13.4050] },
      { name: "Lisbon", coordinates: [38.7223, -9.1393] },
      { name: "Oslo", coordinates: [59.9139, 10.7522] }
    ];

    const markers = cities.map(({ name, coordinates }) =>
      L.marker(coordinates)
        .addTo(map)
        .bindPopup(`<strong>${name}</strong>`)
        .bindTooltip(name)
    );

    const markerGroup = L.featureGroup(markers);
    map.fitBounds(markerGroup.getBounds(), { padding: [40, 40] });

    L.control.scale({ imperial: false }).addTo(map);
  </script>
</body>
</html>