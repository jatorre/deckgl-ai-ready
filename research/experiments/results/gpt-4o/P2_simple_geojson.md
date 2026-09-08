<!-- model: ac_7xhfwyml::openai::gpt-4o | prompt: P2_simple_geojson | seconds: 4 | backend: litellm-proxy | usage: {"completion_tokens": 485, "prompt_tokens": 53, "total_tokens": 538, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
To build a simple interactive web map of world airports using a GeoJSON file, I recommend using the **Leaflet** library. Leaflet is lightweight, easy to use, and widely adopted for creating interactive maps on the web.

Here's a minimal code example to accomplish this task:

1. **Include Leaflet Library**:
   You'll need to include the Leaflet CSS and JS files in your HTML:

   ```html
   <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
   <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
   ```

2. **HTML Structure**:
   Create a `div` to hold your map.

   ```html
   <div id="map" style="height: 500px;"></div>
   ```

3. **JavaScript for Map Initialization**:
   Initialize the map, add tiles, and load the GeoJSON data.

   ```html
   <script>
     // Initialize the map and set its view
     var map = L.map('map').setView([20, 0], 2);

     // Add OpenStreetMap tiles
     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       maxZoom: 18,
     }).addTo(map);

     // Load GeoJSON data (Assuming geojsonData is your GeoJSON object)
     fetch('path_to_your_airports.geojson') // Replace with your GeoJSON file path
       .then(response => response.json())
       .then(geojsonData => {
         // Add GeoJSON layer to the map
         L.geoJSON(geojsonData, {
           onEachFeature: function (feature, layer) {
             // Bind a tooltip with airport name to each feature
             if (feature.properties && feature.properties.name) {
               layer.bindTooltip(feature.properties.name);
             }
           }
         }).addTo(map);
       })
       .catch(error => console.error(error));
   </script>
   ```

Remember to replace `'path_to_your_airports.geojson'` with the actual path to your GeoJSON file containing the airports data. This setup will display a map with points representing airports, and when hovered over, the tooltips will show the respective airport names.