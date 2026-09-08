<!-- model: claude-opus-5 | prompt: P2_simple_geojson | seconds: 17 | backend: claude-cli tools=none -->
## Use MapLibre GL JS

Leaflet is simpler, but a full world-airports GeoJSON is ~80k points — Leaflet renders each as a DOM marker and will stall. MapLibre draws them on the GPU in one layer and gives you cheap hover hit-testing. It's also open source with no API key.

```html
<!DOCTYPE html>
<meta charset="utf-8" />
<link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet" />
<style>
  html, body, #map { margin: 0; height: 100%; }
  .maplibregl-popup-content { font: 13px sans-serif; padding: 6px 10px; }
</style>
<div id="map"></div>
<script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
<script>
  const map = new maplibregl.Map({
    container: 'map',
    style: 'https://demotiles.maplibre.org/style.json',
    center: [0, 20],
    zoom: 1.5
  });

  const popup = new maplibregl.Popup({
    closeButton: false,
    closeOnClick: false
  });

  map.on('load', () => {
    map.addSource('airports', { type: 'geojson', data: 'airports.geojson' });

    map.addLayer({
      id: 'airport-points',
      type: 'circle',
      source: 'airports',
      paint: {
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 2, 2, 10, 6],
        'circle-color': '#e55',
        'circle-stroke-width': 1,
        'circle-stroke-color': '#fff'
      }
    });

    map.on('mousemove', 'airport-points', (e) => {
      const f = e.features[0];
      map.getCanvas().style.cursor = 'pointer';
      popup
        .setLngLat(f.geometry.coordinates)
        .setText(f.properties.name)
        .addTo(map);
    });

    map.on('mouseleave', 'airport-points', () => {
      map.getCanvas().style.cursor = '';
      popup.remove();
    });
  });
</script>
```

Two things to adjust for your data: `f.properties.name` must match your GeoJSON's name field, and `airports.geojson` needs to be served over HTTP (`python3 -m http.server`) — `file://` will be blocked by CORS.

If your file is only a few thousand airports, Leaflet's `L.geoJSON(...).bindTooltip()` is a shorter path. Want me to write these files into your project?
