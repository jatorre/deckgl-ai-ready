<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P3_h3_hexagons | seconds: 6 | backend: litellm-proxy | usage: {"completion_tokens": 1053, "prompt_tokens": 53, "total_tokens": 1106, "completion_tokens_details": {"reasoning_tokens": 379, "text_tokens": 674}, "prompt_tokens_details": {"text_tokens": 53}} -->
### Recommended Libraries

* **deck.gl** (via `@deck.gl/geo-layers`): The industry standard for H3. Its `H3HexagonLayer` natively renders H3 cells directly on the GPU without needing manual GeoJSON conversion.
* **MapLibre GL JS**: High-performance, open-source base map provider (no API key required with free tile services like CARTO/OpenStreetMap).

---

### Minimal Example (Single HTML File)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>H3 deck.gl Map</title>
  <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.css" rel="stylesheet" />
  <style>body { margin: 0; }</style>
</head>
<body>
  <div id="map" style="width: 100vw; height: 100vh;"></div>
  <script>
    // Sample data (San Francisco H3 res-8 cells with counts)
    const data = [
      { hex: "8828308281fffff", count: 120 },
      { hex: "8828308285fffff", count: 350 },
      { hex: "8828308287fffff", count: 800 }
    ];

    const maxCount = Math.max(...data.map(d => d.count));

    new deck.DeckGL({
      container: 'map',
      mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      initialViewState: { longitude: -122.4194, latitude: 37.7749, zoom: 11 },
      controller: true,
      layers: [
        new deck.H3HexagonLayer({
          id: 'h3-layer',
          data,
          getHexagon: d => d.hex,
          getFillColor: d => {
            const intensity = (d.count / maxCount) * 255;
            return [intensity, 50, 255 - intensity, 180]; // Color: Blue -> Red
          },
          getElevation: d => d.count,
          elevationScale: 2,
          extruded: true,
          pickable: true
        })
      ],
      getTooltip: ({object}) => object && `Hex: ${object.hex}\nCount: ${object.count}`
    });
  </script>
</body>
</html>
```