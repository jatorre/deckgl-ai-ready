<!-- model: z-ai/glm-5.3 | prompt: P8_single_html_markers | seconds: 31 | backend: openrouter | usage: {"prompt_tokens": 57, "completion_tokens": 679, "total_tokens": 736, "cost": 0.0029059075, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0029059075, "upstream_inference_prompt_cost": 6.76875e-05, "upstream_inference_completions_cost": 0.00283822}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Interactive City Map

I'll use **Leaflet** with OpenStreetMap tiles—it's lightweight, free, requires no API key, and works perfectly from a CDN in a single file.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>European Cities Map</title>

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

  <style>
    html, body {
      height: 100%;
      margin: 0;
    }
    #map {
      height: 100%;
      width: 100%;
    }
  </style>
</head>
<body>

  <div id="map"></div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <script>
    // City data
    const cities = [
      { name: "Madrid", lat: 40.4168,  lon: -3.7038 },
      { name: "Zurich", lat: 47.3769,  lon: 8.5417  },
      { name: "Berlin", lat: 52.5200,  lon: 13.4050 },
      { name: "Lisbon", lat: 38.7223,  lon: -9.1393 },
      { name: "Oslo",   lat: 59.9139,  lon: 10.7522 }
    ];

    // Initialize the map, centered roughly on Europe
    const map = L.map("map").setView([48.5, 6.0], 4);

    // Add OpenStreetMap tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add a marker with popup for each city
    cities.forEach(city => {
      L.marker([city.lat, city.lon])
        .addTo(map)
        .bindPopup(`<strong>${city.name}</strong>`);
    });
  </script>

</body>
</html>
```

## How it works

- **Leaflet 1.9.4** is loaded from unpkg (both CSS and JS).
- The map is initialized centered on Europe (`[48.5, 6.0]`, zoom level 4) so all five cities are visible at once.
- Each city is stored with its coordinates in a `cities` array, then a loop adds an `L.marker` for each with a bound popup showing the city name.
- Clicking any marker opens its popup; the map supports pan, zoom, and scrolling out of the box.

Just save it as an `.html` file and open it in a browser—no build step or API keys needed.