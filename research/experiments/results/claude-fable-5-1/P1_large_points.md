<!-- model: claude-fable-5-1 | prompt: P1_large_points | seconds: 23 | backend: claude-cli tools=none -->
Use deck.gl for the points on top of a MapLibre GL basemap. Two million points is well within deck.gl's comfort zone if you hand it typed arrays instead of an array of JavaScript objects, so the GPU does the work and there is no per-point JS overhead during pan and zoom.

Stack:

- **Data:** preprocess to a flat binary file (Float32 positions, Uint8 RGB colors) or Apache Arrow. Skip GeoJSON at this scale.
- **Basemap:** MapLibre GL JS with a free vector style such as CARTO Positron.
- **Rendering:** deck.gl `ScatterplotLayer` fed with binary attributes.
- **Build:** Vite, plain JS or React.

Minimal example:

```html
<script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
<link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet">
<script src="https://unpkg.com/deck.gl@9/dist.min.js"></script>
<div id="map" style="height:100vh"></div>
<script>
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  center: [-3.7, 40.4], zoom: 6
});

async function load() {
  const buf = await fetch('/points.bin').then(r => r.arrayBuffer());
  const n = buf.byteLength / 11;             // 8 bytes lng/lat + 3 bytes rgb
  const positions = new Float32Array(buf, 0, n * 2);
  const colors = new Uint8Array(buf, n * 8, n * 3);

  const overlay = new deck.MapboxOverlay({
    interleaved: true,
    layers: [new deck.ScatterplotLayer({
      id: 'gps',
      data: { length: n, attributes: {
        getPosition: { value: positions, size: 2 },
        getFillColor: { value: colors, size: 3 }
      }},
      radiusMinPixels: 1, radiusMaxPixels: 4, getRadius: 5,
      pickable: false
    })]
  });
  map.addControl(overlay);
}
map.on('load', load);
</script>
```

Precompute the speed color ramp server side so the browser never touches per-point logic. If you later need aggregation at low zoom, swap in deck.gl's `GPUGridLayer` or `HexagonLayer` with the same binary data.
