<!-- model: claude-haiku-4-5-20251001 | prompt: P3_h3_hexagons | seconds: 9 | backend: claude-cli tools=none -->
**Recommended Stack:**

1. **Maplibre GL JS** (open-source map renderer) or **Mapbox GL JS** (more polished, paid)
2. **h3-js** (convert H3 indices to polygon boundaries)
3. **GeoJSON** format for the hexagon features

**Why this combo:** Maplibre renders GeoJSON layers efficiently and supports data-driven styling. h3-js converts H3 cell indices to lat/lng polygons in seconds.

**Minimal Example:**

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/maplibre-gl"></script>
  <link href="https://cdn.jsdelivr.net/npm/maplibre-gl/dist/maplibre-gl.css" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/h3-js"></script>
  <style>
    body { margin: 0; }
    #map { height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    // Sample data: H3 indices with counts
    const data = [
      { h3Index: '8828308281fffff', count: 150 },
      { h3Index: '8828308280fffff', count: 200 },
      // ... more rows
    ];

    // Convert to GeoJSON
    const features = data.map(d => ({
      type: 'Feature',
      properties: { count: d.count },
      geometry: h3.cellToBoundary(d.h3Index, true) // true for GeoJSON format
    }));

    const geojson = { type: 'FeatureCollection', features };

    // Initialize map (centered on your city)
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [-87.6298, 41.8781], // Chicago
      zoom: 11
    });

    map.on('load', () => {
      map.addSource('h3-data', { type: 'geojson', data: geojson });
      map.addLayer({
        id: 'h3-layer',
        type: 'fill',
        source: 'h3-data',
        paint: {
          'fill-color': [
            'interpolate', ['linear'], ['get', 'count'],
            0, '#ffffcc',
            500, '#ff0000'
          ],
          'fill-opacity': 0.7
        }
      });
    });
  </script>
</body>
</html>
```

**Key points:**
- `h3.cellToBoundary()` converts H3 indices to polygon coordinates
- Use `interpolate` paint expressions for smooth color gradients
- Add `map.addLayer()` with `line` type for hexagon borders if needed

Done!
