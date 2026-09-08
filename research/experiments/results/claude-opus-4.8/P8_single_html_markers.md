<!-- model: anthropic/claude-opus-4.8 | prompt: P8_single_html_markers | seconds: 19 | backend: openrouter | usage: {"prompt_tokens": 84, "completion_tokens": 1390, "total_tokens": 1474, "cost": 0.03517, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03517, "upstream_inference_prompt_cost": 0.00042, "upstream_inference_completions_cost": 0.03475}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Interactive European Cities Map

Here's a complete single-file HTML page using **Leaflet.js** — a lightweight, popular open-source mapping library that's perfect for this task (no API key required, uses free OpenStreetMap tiles).

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>European Cities Map</title>

    <!-- Leaflet CSS -->
    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""
    />

    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
        }
        #map {
            height: 100%;
            width: 100%;
        }
        .map-title {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(255, 255, 255, 0.9);
            padding: 8px 20px;
            border-radius: 8px;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>

    <div class="map-title">European Cities</div>
    <div id="map"></div>

    <!-- Leaflet JS -->
    <script
        src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin="">
    </script>

    <script>
        // Define the cities with their coordinates
        const cities = [
            { name: "Madrid",  coords: [40.4168, -3.7038] },
            { name: "Zurich",  coords: [47.3769,  8.5417] },
            { name: "Berlin",  coords: [52.5200, 13.4050] },
            { name: "Lisbon",  coords: [38.7223, -9.1393] },
            { name: "Oslo",    coords: [59.9139, 10.7522] }
        ];

        // Initialize the map centered roughly over Western Europe
        const map = L.map('map').setView([48.0, 5.0], 4);

        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add a marker for each city with a popup
        const markers = [];
        cities.forEach(city => {
            const marker = L.marker(city.coords)
                .addTo(map)
                .bindPopup(`<strong>${city.name}</strong>`);
            markers.push(marker);
        });

        // Fit map bounds to show all markers nicely
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.2));
    </script>

</body>
</html>
```

## Key features

- **Leaflet.js** — lightweight (~40 KB), no API key, free OpenStreetMap tiles.
- **5 markers** for Madrid, Zurich, Berlin, Lisbon, and Oslo with accurate coordinates.
- **Clickable popups** showing each city's name.
- **Auto-fit bounds** so all five cities are visible when the page loads.
- **Responsive full-screen map** that works on desktop and mobile.

Just save it as an `.html` file and open it in any browser — no build step or server required.