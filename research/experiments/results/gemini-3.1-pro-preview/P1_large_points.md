<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P1_large_points | seconds: 15 | backend: litellm-proxy | usage: {"completion_tokens": 1858, "prompt_tokens": 66, "total_tokens": 1924, "completion_tokens_details": {"reasoning_tokens": 1248, "text_tokens": 610}, "prompt_tokens_details": {"text_tokens": 66}} -->
To render 2 million points smoothly, standard DOM-based libraries like Leaflet will crash the browser. You must use a **WebGL-accelerated** library that offloads rendering to the GPU.

**Recommendation: deck.gl + MapLibre GL JS**
*   **deck.gl:** A WebGL framework built by Uber explicitly designed for visualizing massive datasets (millions of items) at 60 FPS. 
*   **MapLibre GL JS:** A highly performant, open-source vector map library used as the basemap.

*Production Tip:* While deck.gl can render 2 million points, downloading a massive JSON file will bottleneck the network and browser memory. In production, serve your data as **Vector Tiles** (using PMTiles or Martin) or use binary formats like Apache Arrow.

### Minimal Example (Vanilla JS)

This example uses deck.gl's standalone bundle, which automatically integrates a MapLibre basemap.

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Load deck.gl and MapLibre -->
  <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@latest/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@latest/dist/maplibre-gl.css" rel="stylesheet" />
  <style>body { margin: 0; }</style>
</head>
<body>
  <script>
    // Assuming data is an array of objects: { coords: [lng, lat], speed: 65 }
    const GPS_DATA = 'https://your-api.com/gps-data.json'; 

    const scatterplotLayer = new deck.ScatterplotLayer({
      id: 'gps-points',
      data: GPS_DATA,
      getPosition: d => d.coords,
      // Color by speed: Red if > 50, Green otherwise
      getFillColor: d => d.speed > 50 ? [255, 0, 0, 200] : [0, 255, 0, 200],
      radiusMinPixels: 2,
      pickable: true
    });

    new deck.DeckGL({
      mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
      initialViewState: { longitude: -122.4, latitude: 37.7, zoom: 10 },
      controller: true,
      layers: [scatterplotLayer]
    });
  </script>
</body>
</html>
```