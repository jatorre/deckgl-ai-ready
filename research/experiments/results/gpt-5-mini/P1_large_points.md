<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P1_large_points | seconds: 11 | backend: litellm-proxy reasoning_effort=low max_tokens=8000 | usage: {"completion_tokens": 899, "prompt_tokens": 73, "total_tokens": 972, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 256, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
Recommendation (one concrete stack)
- Data preparation: tippecanoe to convert 2M points into Mapbox Vector Tiles (MBTiles).
- Tile server: tileserver-gl (or serve MBTiles via tileserver or CDN).
- Map library: MapLibre GL JS (open-source Mapbox GL compatible WebGL renderer).
- Optional: use Mapbox/Maptiler basemap or host one via vector tiles.

Why: vector tiles + WebGL rendering keep map smooth at all zooms; styling by speed done on GPU.

Minimal example
1) Build tiles:
- tippecanoe -o points.mbtiles -zp0 -Z14 --drop-densest-as-needed points.geojson

2) Serve points.mbtiles at /tiles/{z}/{x}/{y}.pbf (tileserver-gl or custom).

3) HTML (MapLibre GL JS) — replace YOUR_BASEMAP_STYLE and /tiles endpoint:

<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>2M points by speed</title>
  <meta name="viewport" content="initial-scale=1,width=device-width" />
  <link href="https://unpkg.com/maplibre-gl@2.5.0/dist/maplibre-gl.css" rel="stylesheet"/>
  <script src="https://unpkg.com/maplibre-gl@2.5.0/dist/maplibre-gl.js"></script>
  <style>body,html,#map{height:100%;margin:0}</style>
</head>
<body>
<div id="map"></div>
<script>
const map = new maplibregl.Map({
  container: 'map',
  style: 'YOUR_BASEMAP_STYLE', // e.g. hosted style JSON or MapTiler/OSM style
  center: [-98,39], zoom:4
});
map.on('load', () => {
  map.addSource('points', {
    'type': 'vector',
    'tiles': ['https://your.server/tiles/{z}/{x}/{y}.pbf'],
    'maxzoom': 14
  });
  map.addLayer({
    'id':'points-layer',
    'type':'circle',
    'source':'points',
    'source-layer':'points', // layer name inside mbtiles (check tippecanoe)
    'paint': {
      'circle-radius': 3,
      // color by "speed" property: blue (slow) -> red (fast)
      'circle-color': [
        'interpolate', ['linear'], ['get', 'speed'],
        0, '#2c7bb6',
        30, '#ffffbf',
        60, '#d7191c'
      ],
      'circle-opacity': 0.8
    }
  });
});
</script>
</body>
</html>

Notes
- Tune tippecanoe parameters (zoom, drop-densest) to control tile size and performance.
- Use MapLibre for no-vendor lock-in; Mapbox GL JS is an alternative if you prefer.