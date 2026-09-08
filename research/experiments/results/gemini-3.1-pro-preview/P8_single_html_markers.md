<!-- model: ac_7xhfwyml::vertex::gemini-3.1-pro-preview | prompt: P8_single_html_markers | seconds: 14 | backend: litellm-proxy | usage: {"completion_tokens": 1822, "prompt_tokens": 46, "total_tokens": 1868, "completion_tokens_details": {"reasoning_tokens": 1044, "text_tokens": 778}, "prompt_tokens_details": {"text_tokens": 46}} -->
Here is the complete, single-file HTML code using **Leaflet.js**, which is the most popular and lightweight open-source library for interactive maps. It uses OpenStreetMap tiles and doesn't require any API keys.

You can save this code as an `.html` file (for example, `map.html`) and open it directly in any web browser.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>European Cities Map</title>
    
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />

    <style>
        /* Remove default margins and make the map take up the full screen */
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
        }
        
        #map {
            height: 100%;
            width: 100%;
        }
    </style>
</head>
<body>

    <!-- Map Container -->
    <div id="map"></div>

    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

    <script>
        // Initialize the map and set its view roughly to the center of Western Europe
        const map = L.map('map').setView([49.0, 5.0], 4);

        // Add OpenStreetMap tile layer to the map
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Array of city data containing names and coordinates [Latitude, Longitude]
        const cities = [
            { name: "Madrid", coords: [40.4168, -3.7038] },
            { name: "Zurich", coords: [47.3769, 8.5417] },
            { name: "Berlin", coords: [52.5200, 13.4050] },
            { name: "Lisbon", coords: [38.7223, -9.1393] },
            { name: "Oslo", coords: [59.9139, 10.7522] }
        ];

        // Loop through the cities array and add a marker and popup for each
        cities.forEach(city => {
            L.marker(city.coords)
                .addTo(map)
                .bindPopup(`<h3>${city.name}</h3>`);
        });
    </script>

</body>
</html>
```