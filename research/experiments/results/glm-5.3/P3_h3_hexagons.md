<!-- model: z-ai/glm-5.3 | prompt: P3_h3_hexagons | seconds: 5 | backend: openrouter | usage: {"prompt_tokens": 64, "completion_tokens": 670, "total_tokens": 734, "cost": 0.0030376, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0030376, "upstream_inference_prompt_cost": 8.96e-05, "upstream_inference_completions_cost": 0.002948}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Visualizing H3 Hexagons on an Interactive Map

**Recommended stack:**
- **Leaflet** (lightweight) or **MapLibre GL** (better performance for large datasets)
- **h3-js** to convert H3 indexes to polygon boundaries
- Load via CDN or npm

For >10k hexagons, prefer MapLibre with a GeoJSON source; for smaller data, Leaflet is simpler.

## Minimal Leaflet Example

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
  <script src="https://unpkg.com/h3-js"></script>
  <style> #map { height: 100vh; } </style>
</head>
<body>
<div id="map"></div>
<script>
const data = [
  { h3: "892a1072ab7ffff", count: 12 },
  { h3: "892a1072abfffff", count: 45 },
  // ... more rows
];

const map = L.map("map").setView([37.77, -122.42], 11); // SF
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap"
}).addTo(map);

const maxCount = Math.max(...data.map(d => d.count));

data.forEach(({ h3, count }) => {
  const [lat, lng] = h3.cellToLatLng(h3);
  const boundary = h3.cellToBoundary(h3, true); // [[lat,lng],...]
  L.polygon(
    boundary,
    {
      color: "#333",
      weight: 0.5,
      fillColor: `hsl(${220 - 220 * (count / maxCount)}, 90%, 55%)`,
      fillOpacity: 0.7
    }
  ).bindTooltip(`count: ${count}`).addTo(map);
});
</script>
</body>
</html>
```

**Key API notes:** h3-js v4 uses `h3.cellToBoundary(h3, true)` (returns `[lat, lng]` pairs for Leaflet). In v3 it was `h3ToGeoBoundary`.

## For Large Datasets

Convert to GeoJSON once and use MapLibre GL JS with a `fill` layer — it renders 100k+ polygons smoothly and supports data-driven styling:

```js
const features = data.map(d => ({
  type: "Feature",
  properties: { count: d.count },
  geometry: {
    type: "Polygon",
    coordinates: [h3.cellToBoundary(d.h3, true).map(([lat, lng]) => [lng, lat])]
  }
}));
// add as source, style with ["interpolate", ["linear"], ["get", "count"], ...]
```

Alternative: **deck.gl** has a built-in `H3HexagonLayer` that takes raw H3 indexes directly — best option if you're already in React or need GPU performance.