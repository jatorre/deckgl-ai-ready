<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P2_simple_geojson | seconds: 12 | backend: litellm-proxy | usage: {"completion_tokens": 1123, "prompt_tokens": 52, "total_tokens": 1175, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 704, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Use Leaflet — it's lightweight, easy to use, supports GeoJSON out of the box and tooltips without an API key.

Minimal example (save as index.html, put your GeoJSON as airports.geojson next to it):

<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Airports map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
  <style>html,body,#map{height:100%;margin:0}</style>
</head>
<body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
const map = L.map('map').setView([20,0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);

fetch('airports.geojson')
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data, {
      pointToLayer: (f, latlng) => L.circleMarker(latlng, {radius:4, color:'#0077cc', fillOpacity:0.9}),
      onEachFeature: (feature, layer) => {
        const name = (feature.properties && (feature.properties.name || feature.properties.NAME)) || 'Unknown';
        layer.bindTooltip(name, {direction:'top', offset:[0,-6], sticky:true});
        layer.on('mouseover', e => e.target.openTooltip());
        layer.on('mouseout',  e => e.target.closeTooltip());
      }
    }).addTo(map);
  })
  .catch(console.error);
</script>
</body>
</html>

Notes: adjust property key if your GeoJSON uses a different name field. If you need high-performance rendering for millions of points, consider Mapbox GL JS or deck.gl.