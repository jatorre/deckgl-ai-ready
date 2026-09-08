<!-- model: ac_7xhfwyml::openai::gpt-5-mini | prompt: P5_deckgl_on_maplibre | seconds: 15 | backend: litellm-proxy reasoning_effort=low max_tokens=8000 | usage: {"completion_tokens": 1024, "prompt_tokens": 46, "total_tokens": 1070, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 576, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
npm install --save maplibre-gl @deck.gl/core @deck.gl/layers @deck.gl/maplibre

Minimal ES module example (bundle with webpack/parcel/rollup). Save as index.html + index.js and bundle.

index.html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>MapLibre + deck.gl</title>
    <style>
      html,body,#map { height:100%; margin:0; padding:0; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script type="module" src="./index.js"></script>
  </body>
</html>

index.js
import maplibregl from 'maplibre-gl';
import {ScatterplotLayer} from '@deck.gl/layers';
import {MaplibreLayer} from '@deck.gl/maplibre';

// Create MapLibre map
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json', // public demo style
  center: [-122.45, 37.78],
  zoom: 12
});

map.on('load', () => {
  // deck.gl layer(s)
  const scatter = new ScatterplotLayer({
    id: 'scatter',
    data: [{position: [-122.45, 37.78], size: 100}],
    getPosition: d => d.position,
    getRadius: d => 50,
    getFillColor: [255, 0, 0, 200]
  });

  // Wrap deck.gl layers for MapLibre and add to the map
  const deckLayer = new MaplibreLayer({
    id: 'deck-layer',
    layers: [scatter]
  });

  map.addLayer(deckLayer);
});

Notes:
- Bundle with a tool that supports ES modules (webpack/parcel/rollup).
- You can replace ScatterplotLayer with any deck.gl layer. MaplibreLayer synchronizes deck.gl with the MapLibre GL JS camera.