<!-- model: claude-haiku-4-5-20251001 | prompt: P8_single_html_markers | seconds: 11 | backend: claude-cli tools=none -->
I'll create a single-file HTML page using Leaflet and OpenStreetMap—a lightweight, free option that requires no API keys.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>European Cities Map</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            height: 100vh;
        }
        #map {
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        const map = L.map('map').setView([54.5260, 15.2551], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);

        const cities = [
            { name: 'Madrid', lat: 40.4168, lng: -3.7038 },
            { name: 'Zurich', lat: 47.3769, lng: 8.5472 },
            { name: 'Berlin', lat: 52.5200, lng: 13.4050 },
            { name: 'Lisbon', lat: 38.7223, lng: -9.1393 },
            { name: 'Oslo', lat: 59.9139, lng: 10.7522 }
        ];

        cities.forEach(city => {
            L.marker([city.lat, city.lng])
                .bindPopup(city.name)
                .addTo(map);
        });
    </script>
</body>
</html>
```

This page uses Leaflet with OpenStreetMap tiles. It's entirely self-contained—just save it as an `.html` file and open it in any browser. Each city marker shows its name when clicked.
