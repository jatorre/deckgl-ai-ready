<!-- model: gpt-5.6-sol | prompt: P2_simple_geojson | seconds: 23 | backend: codex-cli sandbox=read-only web_search=disabled -->
Use **MapLibre GL JS**. It’s open-source, fast with large GeoJSON datasets, and provides straightforward hover interactions.

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>World Airports</title>
  <link
    href="https://unpkg.com/maplibre-gl@5/dist/maplibre-gl.css"
    rel="stylesheet"
  />
  <style>
    body { margin: 0; }
    #map { height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/maplibre-gl@5/dist/maplibre-gl.js"></script>
  <script>
    const map = new maplibregl.Map({
      container: "map",
      style: "https://demotiles.maplibre.org/style.json",
      center: [0, 20],
      zoom: 1.5
    });

    map.on("load", () => {
      map.addSource("airports", {
        type: "geojson",
        data: "./airports.geojson"
      });

      map.addLayer({
        id: "airports",
        type: "circle",
        source: "airports",
        paint: {
          "circle-radius": 4,
          "circle-color": "#e63946",
          "circle-stroke-color": "#fff",
          "circle-stroke-width": 1
        }
      });

      const popup = new maplibregl.Popup({
        closeButton: false,
        closeOnClick: false
      });

      map.on("mousemove", "airports", (event) => {
        const airport = event.features[0];

        map.getCanvas().style.cursor = "pointer";
        popup
          .setLngLat(airport.geometry.coordinates)
          .setText(airport.properties.name)
          .addTo(map);
      });

      map.on("mouseleave", "airports", () => {
        map.getCanvas().style.cursor = "";
        popup.remove();
      });
    });
  </script>
</body>
</html>
```

Your GeoJSON should contain `Point` features with a `name` property. Serve the directory through a local web server rather than opening the HTML directly—for example, `python3 -m http.server`.