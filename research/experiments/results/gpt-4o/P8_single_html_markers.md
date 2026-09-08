<!-- model: ac_7xhfwyml::openai::gpt-4o | prompt: P8_single_html_markers | seconds: 6 | backend: litellm-proxy | usage: {"completion_tokens": 655, "prompt_tokens": 52, "total_tokens": 707, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
To create an interactive map with markers for Madrid, Zurich, Berlin, Lisbon, and Oslo using Leaflet.js, you can use the following HTML code. Leaflet.js is a popular open-source JavaScript library for mobile-friendly interactive maps. This example includes the necessary Leaflet.js and CSS files and scripts directly within the HTML file, so it remains a single-file page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Map with Leaflet</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        #map {
            height: 600px;
            width: 100%;
        }
    </style>
</head>
<body>

<h1>Interactive Map with City Markers</h1>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
<script>
    // Initialize the map and set its view to the center of Europe
    var map = L.map('map').setView([50.8503, 10.3513], 5);

    // Add a tile layer to the map (OpenStreetMap layer)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Define the cities and their coordinates
    var cities = [
        {name: 'Madrid', coords: [40.4168, -3.7038]},
        {name: 'Zurich', coords: [47.3769, 8.5417]},
        {name: 'Berlin', coords: [52.5200, 13.4050]},
        {name: 'Lisbon', coords: [38.7223, -9.1393]},
        {name: 'Oslo', coords: [59.9139, 10.7522]}
    ];

    // Add a marker for each city with a popup
    cities.forEach(function(city) {
        L.marker(city.coords).addTo(map)
            .bindPopup(city.name)
            .openPopup();
    });
</script>

</body>
</html>
```

### Instructions:

1. **Save the Code**: Copy the above code into a text file and save it with an `.html` extension, for example, `map.html`.

2. **Open in a Browser**: Open this file in any modern web browser. The map will load with markers on the specified cities.

3. **Map Interaction**: You can zoom in and out using the controls on the left, and click on each marker to see the city name pop up.

This HTML page effectively demonstrates a simple interactive map with Leaflet.js, showing markers for each specified city with popups.