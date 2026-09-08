<!-- model: claude-fable-5-1 | prompt: P2_simple_geojson | seconds: 18 | backend: claude-cli tools=none -->
**Use MapLibre GL JS.** It is open source, renders thousands of airport points smoothly on the GPU, and needs no API key with a free basemap like the demo tiles or OpenFreeMap. Leaflet is simpler for tiny datasets, but world airports are around 7,000 points, where MapLibre stays fast.

Minimal example, assuming `airports.geojson` sits next to the HTML file with a `name` property on each feature:

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet">
  <script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
  <style>html, body, #map { margin: 0; height: 100%; }</style>
</head>
<body>
<div id="map"></div>
<script>
  const map = new maplibregl.Map({
    container: 'map',
    style: 'https://tiles.openfreemap.org/styles/positron',
    center: [0, 20],
    zoom: 1.5
  });

  map.on('load', () => {
    map.addSource('airports', { type: 'geojson', data: 'airports.geojson' });
    map.addLayer({
      id: 'airports',
      type: 'circle',
      source: 'airports',
      paint: { 'circle-radius': 3, 'circle-color': '#e63946' }
    });

    const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false });

    map.on('mousemove', 'airports', (e) => {
      map.getCanvas().style.cursor = 'pointer';
      popup.setLngLat(e.features[0].geometry.coordinates)
           .setText(e.features[0].properties.name)
           .addTo(map);
    });

    map.on('mouseleave', 'airports', () => {
      map.getCanvas().style.cursor = '';
      popup.remove();
    });
  });
</script>
</body>
</html>
```

Serve the folder with any static server, since browsers block `fetch` of local files opened directly:

```bash
npx serve .
```

If you later want clustering, add `cluster: true` to the source. If you outgrow GeoJSON, switch the source to vector tiles without changing the layer code.
