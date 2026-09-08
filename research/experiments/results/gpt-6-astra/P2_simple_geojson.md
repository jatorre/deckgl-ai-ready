<!-- model: openai/gpt-6-astra | prompt: P2_simple_geojson | seconds: 12 | backend: openrouter | usage: {"prompt_tokens": 52, "completion_tokens": 604, "total_tokens": 656, "cost": 0.03072, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03072, "upstream_inference_prompt_cost": 0.00052, "upstream_inference_completions_cost": 0.0302}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
Use **Leaflet**: it’s lightweight, easy to set up, and supports GeoJSON and hover tooltips out of the box.

Save your data as `airports.geojson`, with Point features containing a `name` property:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Heathrow Airport" },
      "geometry": {
        "type": "Point",
        "coordinates": [-0.4543, 51.47]
      }
    }
  ]
}
```

Save this as `index.html` in the same directory:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>World airports</title>
  <link rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    html, body, #map { height: 100%; margin: 0; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const map = L.map("map", { preferCanvas: true })
      .setView([20, 0], 2);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(map);

    fetch("./airports.geojson")
      .then(response => {
        if (!response.ok) throw new Error("Could not load airports");
        return response.json();
      })
      .then(data => {
        L.geoJSON(data, {
          pointToLayer: (feature, latlng) =>
            L.circleMarker(latlng, {
              radius: 4,
              color: "#1769aa",
              fillOpacity: 0.8
            }),
          onEachFeature: (feature, layer) => {
            const label = document.createElement("span");
            label.textContent = feature.properties?.name ?? "Unknown airport";
            layer.bindTooltip(label);
          }
        }).addTo(map);
      })
      .catch(console.error);
  </script>
</body>
</html>
```

Serve the directory locally rather than opening the HTML directly:

```bash
python -m http.server 8000
```

Visit `http://localhost:8000`. Hover over an airport dot to see its name. GeoJSON coordinates are **[longitude, latitude]**.