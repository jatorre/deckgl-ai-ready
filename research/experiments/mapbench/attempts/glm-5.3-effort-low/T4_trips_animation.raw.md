```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NYC Taxi Trips — deck.gl × MapLibre GL</title>

<!-- Typography -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">

<!-- Map & layer libraries: UMD builds from a public CDN, no bundler, no keys -->
<link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet">
<script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/deck.gl@^8.9.0/dist.min.js"></script>

<style>
:root{
  --ink:#e9edf2;
  --ink-dim:#96a3af;
  --panel-bg:rgba(11,14,18,.74);
  --panel-line:rgba(255,255,255,.09);
  --vendor0:#fd805d;
  --vendor1:#17b8be;
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;overflow:hidden;background:#0a0c0f;color:var(--ink);
  font-family:'Space Grotesk',sans-serif;
  -webkit-font-smoothing:antialiased;
}

/* Map stack: MapLibre canvas below, deck.gl canvas above (transparent, inert) */
#stage{position:fixed;inset:0}
#map{position:absolute;inset:0}
#deck-canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}

/* HUD panels */
.hud{position:absolute;z-index:2;user-select:none}
.panel{
  background:var(--panel-bg);
  border:1px solid var(--panel-line);
  border-radius:12px;
  -webkit-backdrop-filter:blur(12px);
  backdrop-filter:blur(12px);
  box-shadow:0 10px 30px rgba(0,0,0,.35);
}

#title-panel{top:16px;left:16px;padding:13px 16px 14px;max-width:min(380px,calc(100vw - 32px))}
#title-panel h1{margin:0;font-size:13px;font-weight:600;letter-spacing:.18em;text-transform:uppercase}
#subtitle{margin:6px 0 0;font-size:12px;line-height:1.55;color:var(--ink-dim)}
#subtitle.loading{animation:pulse 1.4s ease-in-out infinite}
#subtitle.error{color:#e6a05c}
@keyframes pulse{50%{opacity:.4}}

/* Playback controls */
#controls{left:16px;bottom:16px;display:flex;align-items:center;gap:16px;padding:12px 18px 14px;max-width:calc(100vw - 32px);flex-wrap:wrap}

#play-btn{
  flex:none;width:46px;height:46px;border-radius:50%;
  border:1px solid var(--panel-line);background:rgba(255,255,255,.07);
  color:var(--ink);cursor:pointer;display:grid;place-items:center;
  transition:background .18s ease,border-color .18s ease;
}
#play-btn:hover{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.22)}
#play-btn:focus-visible{outline:2px solid rgba(23,184,190,.85);outline-offset:3px}
#play-btn svg{width:20px;height:20px;fill:currentColor;display:block}
#play-btn .icon-play{display:none}
body.paused #play-btn .icon-play{display:block}
body.paused #play-btn .icon-pause{display:none}

.time-block{display:flex;flex-direction:column;min-width:12ch}
.caption{font-size:10px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-dim)}
#time-readout{margin-top:3px;font-family:var(--mono);font-size:24px;font-weight:500;line-height:1.1;font-variant-numeric:tabular-nums;min-width:7ch}
.progress{margin-top:7px;height:3px;border-radius:2px;background:rgba(255,255,255,.13);overflow:hidden}
#progress-fill{height:100%;width:100%;border-radius:2px;background:#dfe6ec;transform:scaleX(0);transform-origin:0 50%}
.meta{margin-top:6px;font-family:var(--mono);font-size:10px;letter-spacing:.05em;color:var(--ink-dim)}

.divider{width:1px;align-self:stretch;background:var(--panel-line)}

.legend{display:flex;flex-direction:column;gap:8px;font-size:12px}
.legend-row{display:flex;align-items:center;gap:9px;white-space:nowrap}
.swatch{width:16px;height:3px;border-radius:2px;flex:none}
.legend-row .count{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--ink-dim)}

/* MapLibre chrome, re-skinned to sit on the dark basemap */
.maplibregl-ctrl{z-index:3}
.maplibregl-ctrl-group{
  background:var(--panel-bg);border:1px solid var(--panel-line);border-radius:10px;overflow:hidden;
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
  box-shadow:0 10px 30px rgba(0,0,0,.3);
}
.maplibregl-ctrl-group button{background-color:transparent}
.maplibregl-ctrl-group button:hover{background-color:rgba(255,255,255,.09)}
.maplibregl-ctrl-group button+button{border-top:1px solid rgba(255,255,255,.09)}
.maplibregl-ctrl button .maplibregl-ctrl-icon{filter:invert(.82)}
.maplibregl-ctrl-attrib{background:rgba(11,14,18,.7);font-size:10px;color:#8b98a4}
.maplibregl-ctrl-attrib a{color:#8b98a4}
.maplibregl-ctrl-attrib-button{filter:invert(.72)}
.maplibregl-ctrl-scale{border-color:rgba(255,255,255,.4);border-top:none;color:var(--ink-dim);font-size:10px}

@media (max-width:640px){
  #controls{gap:12px}
  .divider{display:none}
  #time-readout{font-size:20px}
}
</style>
</head>
<body>

<div id="stage">
  <div id="map"></div>
  <canvas id="deck-canvas"></canvas>
</div>

<header class="hud panel" id="title-panel">
  <h1>NYC Taxi Trips</h1>
  <p id="subtitle" class="loading">Loading trips…</p>
</header>

<div class="hud panel" id="controls">
  <button id="play-btn" aria-label="Pause animation">
    <svg class="icon-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>
    <svg class="icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
  </button>

  <div class="time-block">
    <span class="caption">Playback time</span>
    <span id="time-readout">— s</span>
    <div class="progress"><div id="progress-fill"></div></div>
    <span class="meta" id="meta-line"></span>
  </div>

  <div class="divider" aria-hidden="true"></div>

  <div class="legend">
    <div class="legend-row">
      <span class="swatch" style="background:var(--vendor0)"></span>
      <span>Vendor 0</span><span class="count" id="legend-v0-count">· —</span>
    </div>
    <div class="legend-row">
      <span class="swatch" style="background:var(--vendor1)"></span>
      <span>Vendor 1</span><span class="count" id="legend-v1-count">· —</span>
    </div>
  </div>
</div>

<script>
(function () {
  'use strict';

  /* ------------------------------------------------------------------ config */
  const DATA_URL  = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';
  const STYLE_URL = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json'; // token-free dark basemap

  const VIEW = {longitude: -74.00, latitude: 40.72, zoom: 12, pitch: 45, bearing: 0};
  const VENDOR_COLORS = [
    [253, 128, 93, 255],  // vendor 0 — coral
    [23, 184, 190, 255]  // vendor 1 — teal
  ];
  const TRAIL_SECONDS = 180;  // trail length, in data seconds
  const LOOP_SECONDS  = 60;   // one full pass of the data, in real seconds

  const el = id => document.getElementById(id);
  const subtitle = el('subtitle'), readout = el('time-readout'),
        progressFill = el('progress-fill'), playBtn = el('play-btn');

  el('meta-line').textContent = LOOP_SECONDS + ' s loop · ' + TRAIL_SECONDS + ' s trail';

  if (!window.deck || !window.maplibregl) {
    subtitle.classList.remove('loading');
    subtitle.classList.add('error');
    subtitle.textContent = 'Map libraries failed to load — check network access to unpkg.com.';
    return;
  }

  /* ------------------------------------------------- basemap + deck overlay */
  // MapLibre owns the camera and all interaction; the deck.gl canvas sits on
  // top, draws only the trips, and lets every pointer event pass through.
  const map = new maplibregl.Map({
    container: 'map',
    style: STYLE_URL,
    center: [VIEW.longitude, VIEW.latitude],
    zoom: VIEW.zoom,
    pitch: VIEW.pitch,
    bearing: VIEW.bearing
  });
  map.addControl(new maplibregl.NavigationControl({visualizePitch: true}));
  map.addControl(new maplibregl.ScaleControl(), 'bottom-right');

  const deckgl = new deck.Deck({
    canvas: 'deck-canvas',
    controller: false,
    initialViewState: {...VIEW},
    layers: []
  });

  // Keep deck's camera glued to the basemap camera
  function syncView() {
    const c = map.getCenter();
    deckgl.setProps({
      viewState: {
        longitude: c.lng, latitude: c.lat,
        zoom: map.getZoom(), pitch: map.getPitch(), bearing: map.getBearing()
      }
    });
  }
  map.on('move', syncView);
  map.on('rotate', syncView);
  map.on('pitch', syncView);
  map.on('resize', syncView);

  /* ------------------------------------------------------------------ state */
  let trips = null;
  let tMin = 0, tMax = 0, tSpan = 0;
  let loopClock = 0;            // position within the 60 s real-time loop
  let playing = true;
  let lastFrame = performance.now();

  const fmt = n => Math.round(n).toLocaleString('en-US');

  function setPlaying(v) {
    playing = v;
    document.body.classList