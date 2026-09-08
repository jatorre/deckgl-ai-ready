```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>NYC Trips — deck.gl</title>
<script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
<link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
<script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
<style>
  html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
  #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
  #controls {
    position: absolute; top: 12px; left: 12px; z-index: 10;
    display: flex; align-items: center; gap: 10px;
    background: rgba(0,0,0,0.7); color: #fff;
    padding: 8px 12px; border-radius: 6px;
    font-family: monospace; font-size: 14px;
  }
  #playPause {
    background: #1a73e8; color: #fff; border: none; border-radius: 4px;
    padding: 5px 12px; font-size: 14px; cursor: pointer; font-family: monospace;
  }
  #playPause:hover { background: #4a90e8; }
  #legend { position: absolute; bottom: 12px; left: 12px; z-index: 10;
    background: rgba(0,0,0,0.7); color: #fff; padding: 8px 12px;
    border-radius: 6px; font-family: monospace; font-size: 13px; }
  .swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; }
</style>
</head>
<body>
<div id="map"></div>
<div id="controls">
  <button id="playPause">Pause</button>
  <span>time: <span id="timeReadout">6</span>s</span>
</div>
<div id="legend">
  <span class="swatch" style="background:#17d3ff"></span>Vendor 0&nbsp;&nbsp;
  <span class="swatch" style="background:#ff5bab"></span>Vendor 1
</div>

<script>
const TRIPS_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';

const LOOP_MIN_TIME = 6;          // seconds, min timestamp in data
const LOOP_MAX_TIME = 2487;       // seconds, max timestamp in data
const LOOP_DURATION = LOOP_MAX_TIME - LOOP_MIN_TIME; // data seconds per loop
const REAL_LOOP_MS = 60000;       // one full pass = 60 real seconds
const TRAIL_LENGTH = 180;         // seconds of trail

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  center: [-74.00, 40.72],
  zoom: 12,
  pitch: 45,
  bearing: 0
});

let playing = true;
let currentTime = LOOP_MIN_TIME;
let lastFrame = null;

const tripsLayer = new deck.TripsLayer({
  id: 'trips',
  data: TRIPS_URL,
  getPath: d => d.path,
  getTimestamps: d => d.timestamps,
  getColor: d => d.vendor === 0 ? [23, 211, 255] : [255, 91, 171],
  opacity: 0.8,
  widthMinPixels: 2,
  rounded: true,
  trailLength: TRAIL_LENGTH,
  currentTime
});

map.on('load', () => {
  map.addControl(new deck.MapboxOverlay({ layers: [tripsLayer] }));
  requestAnimationFrame(animate);
});

function animate(now) {
  if (lastFrame === null) lastFrame = now;
  const dt = now - lastFrame;
  lastFrame = now;

  if (playing) {
    const dataSecondsPerMs = LOOP_DURATION / REAL_LOOP_MS;
    currentTime += dt * dataSecondsPerMs;
    if (currentTime > LOOP_MAX_TIME) currentTime = LOOP_MIN_TIME + (currentTime - LOOP_MAX_TIME);
    document.getElementById('timeReadout').textContent = currentTime.toFixed(1);
    tripsLayer.props.currentTime = currentTime;
    // force layer prop update
    tripsLayer.setState({ currentTime });
  }
  requestAnimationFrame(animate);
}

document.getElementById('playPause').addEventListener('click', function () {
  playing = !playing;
  this.textContent = playing ? 'Pause' : 'Play';
});
</script>
</body>
</html>
```