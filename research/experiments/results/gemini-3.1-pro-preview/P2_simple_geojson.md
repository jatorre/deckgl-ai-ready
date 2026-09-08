<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P2_simple_geojson | seconds: 11 | backend: litellm-proxy | usage: {"completion_tokens": 1398, "prompt_tokens": 47, "total_tokens": 1445, "completion_tokens_details": {"reasoning_tokens": 799, "text_tokens": 599}, "prompt_tokens_details": {"text_tokens": 47}} -->
You should use **Leaflet.js**. It is the most popular, lightweight, and open-source JavaScript library for interactive maps. It is beginner-friendly and handles GeoJSON data natively. 

Here is a minimal, complete example. It uses OpenStreetMap for the base map, fetches a local `airports.geojson` file, and uses `bindTooltip` to show the airport name on hover.

```html
<!DOCTYPE html>
<html>
<head>
  <title>World Airports Map</title>
  <!-- Load Leaflet CSS and JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    body { margin: 0; padding: 0; }
    #map { height: 100vh; width: 100vw; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script>
    // 1. Initialize the map centered on the world
    const map = L.map('map').setView([20, 0], 2);

    // 2. Add a base tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 3. Load and display the GeoJSON
    // Replace 'airports.geojson' with the path to your file
    fetch('airports.geojson')
      .then(response => response.json())
      .then(data => {
        L.geoJSON(data, {
          // 4. Add hover tooltip to each point
          onEachFeature: (feature, layer) => {
            if (feature.properties && feature.properties.name) {
              layer.bindTooltip(feature.properties.name);
            }
          }
        }).addTo(map);
      })
      .catch(err => console.error("Error loading GeoJSON:", err));
  </script>
</body>
</html>
```

### How to use this:
1. Save the code as `index.html`.
2. Place your GeoJSON file in the same folder and name it `airports.geojson` (ensure your data has a `properties.name` attribute).
3. Because browsers block local file fetching (CORS), you must run a local web server (e.g., `python -m http.server` or VS Code's "Live Server" extension) to view it.