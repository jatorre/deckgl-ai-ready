```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>NYC Taxi Trips — Animated Trails</title>
<script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
<script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
<link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
<style>
  html, body {
    margin: 0; padding: 0; width: 100%; height: 100%;
    overflow: hidden; background: #000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #e8eef5;
  }
  #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

  .panel {
    position: absolute;
    backdrop-filter: blur(12px);
    background: rgba(14, 18, 28, 0.72);
    border: 1px solid rgba(120, 160, 220, 0.18);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }

  #title {
    top: 20px; left: 20px;
    padding: 16px 20px;
    max-width: 340px;
  }
  #title h1 {
    margin: 0 0 6px;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.3px;
    background: linear-gradient(90deg, #4fd1c5, #f6ad55);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  #title p {
    margin: 0;
    font-size: 12.5px;
    line-height: 1.5;
    color: #9db0c8;
  }

  #legend {
    bottom: 20px; left: 20px;
    padding: 14px 18px;
    font-size: 12px;
  }
  #legend .row { display: flex; align-items: center; margin: 5px 0; }
  #legend .swatch {
    width: 22px; height: 8px; border-radius: 4px; margin-right: 10px;
  }
  #legend .t { color: #b9c6d8; }
  #legend h3 {
    margin: 0 0 8px; font-size: 11px; text-transform: uppercase;
    letter-spacing: 1.2px; color: #7d90a8; font-weight: 600;
  }

  #controls {
    bottom: 20px; right: 20px;
    padding: 14px 18px;
    width: 240px;
    font-size: 12px;
  }
  #controls h3 {
    margin: 0 0 10px; font-size: 11px; text-transform: uppercase;
    letter-spacing: 1.2px; color: #7d90a8; font-weight: 600;
  }
  #clock {
    font-variant-numeric: tabular-nums;
    font-size: 15px; font-weight: 600; color: #f6ad55;
    margin-bottom: 10px;
  }
  .ctl { display: flex; align-items: center; justify-content: space-between; margin: 8px 0; }
  .ctl label { color: #9db0c8; }
  input[type=range] { width: 120px; accent-color: #4fd1c5; }
  button {
    background: rgba(79,209,197,0.15);
    border: 1px solid rgba(79,209,197,0.4);
    color: #4fd1c5;
    border-radius: 6px; padding: 5px 12px; cursor: pointer;
    font-size: 12px; transition: background 0.15s;
  }
  button:hover { background: rgba(79,209,197,0.3); }

  #loading {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 14px; color: #9db0c8; letter-spacing: 0.5px;
  }
</style>
</head>
<body>
<div id="map"></div>

<div id="title" class="panel">
  <h1>New York City · Taxi Trips</h1>
  <p>996 yellow-cab journeys through Manhattan, replayed as glowing animated trails over a single ~41-minute window. Vendor A and Vendor B are shown in distinct hues.</p>
</div>

<div id="legend" class="panel">
  <h3>Vendor</h3>
  <div class="row"><div class="swatch" style="background:linear-gradient(90deg,#00c6ff,#0072ff)"></div><span class="t">Vendor A (0)</span></div>
  <div class="row"><div class="swatch" style="background:linear-gradient(90deg,#ffe259,#ffa751)"></div><span class="t">Vendor B (1)</span></div>
</div>

<div id="controls" class="panel">
  <h3>Playback</h3>
  <div id="clock">00:00</div>
  <div class="ctl">
    <label>Speed</label>
    <input id="speed" type="range" min="1" max="60" value="18" />
  </div>
  <div class="ctl">
    <label>Trail length</label>
    <input id="trail" type="range" min="20" max="400" value="180" />
  </div>
  <div class="ctl">
    <button id="playBtn">⏸ Pause</button>
    <button id="camBtn">🎥 Cinematic: On</button>
  </div>
</div>

<div id="loading">Loading NYC taxi trips…</div>

<script>
const {DeckGL, TripsLayer, MapView, AmbientLight, PointLight, LightingEffect} = deck;

const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';

const INITIAL_VIEW_STATE = {
  longitude: -74.0,
  latitude: 40.72,
  zoom: 13,
  pitch: 45,
  bearing: 0
};

// Token-free dark basemap style (CARTO dark matter, no API key required)
const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

const LOOP_LENGTH = 2500;   // slightly beyond max timestamp (~2487)
const MIN_TIME = 0;

// Vendor colors
const VENDOR_COLORS = [
  [0, 168, 255],    // Vendor A - cyan/blue
  [255, 167, 81]    // Vendor B - amber/orange
];

let animationSpeed = 18;
let trailLength = 180;
let playing = true;
let cinematic = true;
let currentTime = MIN_TIME;
let lastFrame = null;
let tripsData = [];

// Lighting for depth on trails
const ambientLight = new AmbientLight({color: [255,255,255], intensity: 1.0});
const pointLight = new PointLight({color: [255,255,255], intensity: 2.0, position: [-74.0, 40.72, 8000]});
const lightingEffect = new LightingEffect({ambientLight, pointLight});

const deckgl = new DeckGL({
  container: 'map',
  mapStyle: MAP_STYLE,
  initialViewState: INITIAL_VIEW_STATE,
  controller: true,
  views: new MapView({repeat: true}),
  effects: [lightingEffect],
  parameters: { clearColor: [0.02, 0.03, 0.06, 1] }
});

function getColor(d) {
  return VENDOR_COLORS[d.vendor] || VENDOR_COLORS[0];
}

function buildLayers() {
  return [
    new TripsLayer({
      id: 'trips',
      data: tripsData,
      getPath: d => d.path,
      getTimestamps: d => d.timestamps,
      getColor: d => getColor(d),
      opacity: 0.85,
      widthMinPixels: 3,
      rounded: true,
      trailLength: trailLength,
      currentTime: currentTime,
      shadowEnabled: false,
      jointRounded: true,
      capRounded: true
    })
  ];
}

function render() {
  deckgl.setProps({ layers: buildLayers() });
}

function fmtTime(t) {
  const total = Math.floor(t);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
}

const clockEl = document.getElementById('clock');

function animate(ts) {
  if (lastFrame == null) lastFrame = ts;
  const dt = (ts - lastFrame) / 1000; // seconds
  lastFrame = ts;

  if (playing) {
    currentTime += dt * animationSpeed;
    if (currentTime > LOOP_LENGTH) currentTime = MIN_TIME + (currentTime - LOOP_LENGTH);
    clockEl.textContent = fmtTime(currentTime);
    render();
  }

  if (cinematic) {
    // slow continuous camera orbit around Manhattan
    const vs = deckgl.viewManager ? null : null;
    cameraBearing += dt * 1.8; // deg per sec
    if (cameraBearing >= 360) cameraBearing -= 360;
    deckgl.setProps({
      viewState: {
        ...cameraState,
        bearing: cameraBearing
      }
    });
  }

  requestAnimationFrame(animate);
}

// Camera state used for cinematic mode
let cameraBearing = INITIAL_VIEW_STATE.bearing;
let cameraState = { ...INITIAL_VIEW_STATE };

// Allow user interaction to update the base camera state when cinematic off
deckgl.setProps({
  onViewStateChange: ({viewState}) => {
    cameraState = viewState;
    cameraBearing = viewState.bearing;
    if (!cinematic) {
      deckgl.setProps({ viewState });
    }
    return viewState;
  }
});

// Load data
fetch(DATA_URL)
  .then(r => {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  })
  .then(data => {
    tripsData = (data || []).filter(d => d && Array.isArray(d.path) && Array.isArray(d.timestamps) && d.path.length > 1);
    document.getElementById('loading').style.display = 'none';
    render();
    requestAnimationFrame(animate);
  })
  .catch(err => {
    document.getElementById('loading').textContent = 'Failed to load data: ' + err.message;
    console.error(err);
  });

// Controls
document.getElementById('speed').addEventListener('input', e => {
  animationSpeed = Number(e.target.value);
});
document.getElementById('trail').addEventListener('input', e => {
  trailLength = Number(e.target.value);
  render();
});
document.getElementById('playBtn').addEventListener('click', e => {
  playing = !playing;
  e.target.textContent = playing ? '⏸ Pause' : '▶ Play';
});
document.getElementById('camBtn').addEventListener('click', e => {
  cinematic = !cinematic;
  e.target.textContent = cinematic ? '🎥 Cinematic: On' : '🎥 Cinematic: Off';
  if (!cinematic) {
    // hand control back cleanly
    deckgl.setProps({ viewState: undefined, initialViewState: cameraState });
  }
});
</script>
</body>
</html>
```