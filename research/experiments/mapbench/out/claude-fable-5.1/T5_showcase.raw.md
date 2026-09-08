```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Manhattan in Motion — 996 NYC Taxi Trips</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/deck.gl@9.0.35/dist.min.js"></script>
<style>
  :root {
    --bg: rgba(9, 13, 21, 0.76);
    --line: rgba(255, 255, 255, 0.09);
    --text: #e9edf4;
    --muted: #a3adbf;
    --amber: #ffb03b;
    --cyan: #38d6ff;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; height: 100%; overflow: hidden;
    background: #070a10; color: var(--text);
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  #map { position: absolute; inset: 0; }
  #map canvas { outline: none; }

  .panel {
    position: absolute; z-index: 10;
    background: var(--bg);
    -webkit-backdrop-filter: blur(16px) saturate(150%);
    backdrop-filter: blur(16px) saturate(150%);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05);
  }

  /* ---------- Title card ---------- */
  #title { top: 20px; left: 20px; width: 360px; padding: 20px 22px 18px; }
  #title .eyebrow {
    font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--amber); margin-bottom: 8px;
  }
  #title h1 { margin: 0 0 8px; font-size: 24px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.15; }
  #title p.caption { margin: 0; font-size: 13px; line-height: 1.55; color: var(--muted); }
  .stats { display: flex; gap: 18px; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--line); }
  .stat .v { font-size: 17px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .stat .k { font-size: 11px; color: var(--muted); letter-spacing: 0.04em; text-transform: uppercase; margin-top: 2px; }

  .legend { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--line); }
  .legend .row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: 12.5px; }
  .legend .row:last-child { margin-bottom: 0; }
  .legend .trail {
    flex: 0 0 96px; height: 6px; border-radius: 3px; position: relative;
  }
  .legend .trail::after {
    content: ""; position: absolute; right: -2px; top: -3px; width: 12px; height: 12px; border-radius: 50%;
    background: inherit; box-shadow: 0 0 10px 2px currentColor;
  }
  .legend .t0 { color: var(--amber); background: linear-gradient(90deg, rgba(255,176,59,0) 0%, rgba(255,176,59,1) 100%); }
  .legend .t1 { color: var(--cyan);  background: linear-gradient(90deg, rgba(56,214,255,0) 0%, rgba(56,214,255,1) 100%); }
  .legend .note { font-size: 11.5px; color: var(--muted); margin-top: 10px; line-height: 1.45; }
  .legend .note b { color: var(--text); font-weight: 500; }

  /* ---------- Control panel ---------- */
  #controls { left: 20px; bottom: 20px; width: 360px; padding: 16px 18px 16px; }
  .transport { display: flex; align-items: center; gap: 12px; }
  .btn {
    appearance: none; border: 1px solid var(--line); background: rgba(255,255,255,0.06); color: var(--text);
    border-radius: 10px; cursor: pointer; font: inherit; font-size: 12px; font-weight: 500;
    padding: 8px 12px; transition: background .15s, border-color .15s;
  }
  .btn:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.18); }
  .btn.icon { width: 40px; height: 40px; padding: 0; display: grid; place-items: center; font-size: 15px; }
  .clock { display: flex; flex-direction: column; flex: 1; }
  .clock .time { font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; letter-spacing: 0.01em; line-height: 1; }
  .clock .sub { font-size: 11.5px; color: var(--muted); margin-top: 4px; }
  .clock .sub b { color: var(--text); font-weight: 600; font-variant-numeric: tabular-nums; }
  .bar { margin: 14px 0 6px; height: 5px; border-radius: 3px; background: rgba(255,255,255,0.1); cursor: pointer; position: relative; }
  .bar i {
    display: block; height: 100%; width: 0; border-radius: 3px;
    background: linear-gradient(90deg, var(--amber), var(--cyan));
    box-shadow: 0 0 10px rgba(56,214,255,0.35);
  }
  .bar-labels { display: flex; justify-content: space-between; font-size: 10.5px; color: var(--muted); font-variant-numeric: tabular-nums; }

  .sliders { margin-top: 12px; display: grid; gap: 10px; }
  .slider label { display: flex; justify-content: space-between; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
  .slider label output { color: var(--text); font-weight: 500; font-variant-numeric: tabular-nums; }
  input[type=range] { width: 100%; margin: 0; accent-color: var(--amber); cursor: pointer; }

  .toggles { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--line); display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
  .toggle { display: flex; align-items: center; gap: 8px; font-size: 12.5px; cursor: pointer; user-select: none; }
  .toggle input { accent-color: var(--amber); width: 15px; height: 15px; margin: 0; cursor: pointer; }
  .sw { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
  .sw.v0 { background: var(--amber); box-shadow: 0 0 8px rgba(255,176,59,0.6); }
  .sw.v1 { background: var(--cyan);  box-shadow: 0 0 8px rgba(56,214,255,0.6); }
  .footer { margin-top: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--muted); }
  .footer kbd { font: inherit; font-size: 10px; border: 1px solid var(--line); border-radius: 4px; padding: 1px 5px; background: rgba(255,255,255,0.05); }

  /* ---------- Camera badge ---------- */
  #camera-badge {
    position: absolute; z-index: 10; top: 20px; right: 20px; padding: 8px 12px;
    font-size: 11.5px; color: var(--muted); display: flex; align-items: center; gap: 8px;
  }
  #camera-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }
  #camera-badge.paused .dot { background: #8a93a5; box-shadow: none; }

  /* ---------- Loading ---------- */
  #loading {
    position: absolute; inset: 0; z-index: 50; display: grid; place-items: center;
    background: radial-gradient(ellipse at center, rgba(12,18,30,0.6), rgba(7,10,16,0.92));
    transition: opacity .6s ease;
  }
  #loading.hidden { opacity: 0; pointer-events: none; }
  #loading .card { text-align: center; }
  .spinner {
    width: 44px; height: 44px; margin: 0 auto 16px; border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.1); border-top-color: var(--amber); border-right-color: var(--cyan);
    animation: spin 1s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #loading .msg { font-size: 14px; color: var(--muted); }
  #loading .msg.error { color: #ff7b7b; max-width: 360px; line-height: 1.5; }

  .maplibregl-ctrl-attrib { font-family: Inter, sans-serif; font-size: 10px; background: rgba(9,13,21,0.6) !important; color: var(--muted) !important; }
  .maplibregl-ctrl-attrib a { color: var(--muted) !important; }

  @media (max-width: 820px) {
    #title { width: calc(100vw - 40px); }
    #title p.caption, .legend .note { display: none; }
    #controls { width: calc(100vw - 40px); }
    #camera-badge { display: none; }
  }
</style>
</head>
<body>

<div id="map"></div>

<section id="title" class="panel">
  <div class="eyebrow">deck.gl · TripsLayer · New York City</div>
  <h1>Manhattan in Motion</h1>
  <p class="caption">
    996 real yellow-cab journeys replayed against the skyline of Lower Manhattan. Each glowing trail is one taxi;
    its head marks where the cab is right now, and the tail fades as the seconds pass.
  </p>
  <div class="stats">
    <div class="stat"><div class="v" id="stat-trips">—</div><div class="k">trips</div></div>
    <div class="stat"><div class="v" id="stat-points">—</div><div class="k">GPS points</div></div>
    <div class="stat"><div class="v" id="stat-window">—</div><div class="k">time window</div></div>
  </div>
  <div class="legend">
    <div class="row"><span class="trail t0"></span><span>Vendor 0</span></div>
    <div class="row"><span class="trail t1"></span><span>Vendor 1</span></div>
    <div class="note"><b>Drag</b> to orbit, <b>scroll</b> to zoom, <b>hover</b> a trail for details. The camera drifts on its own and resumes a few seconds after you let go.</div>
  </div>
</section>

<section id="controls" class="panel">
  <div class="transport">
    <button class="btn icon" id="play" title="Play / pause (Space)">❚❚</button>
    <div class="clock">
      <div class="time" id="clock">00:00</div>
      <div class="sub"><b id="active">0</b> taxis on the road</div>
    </div>
    <button class="btn" id="reset" title="Return to the initial view">Reset view</button>
  </div>
  <div class="bar" id="bar" title="Click to seek"><i id="bar-fill"></i></div>
  <div class="bar-labels"><span>00:00</span><span id="loop-end">—</span></div>

  <div class="sliders">
    <div class="slider">
      <label>Playback speed <output id="speed-out">60×</output></label>
      <input type="range" id="speed" min="5" max="240" step="5" value="60">
    </div>
    <div class="slider">
      <label>Trail length <output id="trail-out">180 s</output></label>
      <input type="range" id="trail" min="30" max="600" step="10" value="180">
    </div>
  </div>

  <div class="toggles">
    <label class="toggle"><input type="checkbox" id="cinematic" checked> Cinematic camera</label>
    <label class="toggle"><input type="checkbox" id="buildings" checked> 3D buildings</label>
    <label class="toggle"><input type="checkbox" id="v0" checked> <span class="sw v0"></span> Vendor 0</label>
    <label class="toggle"><input type="checkbox" id="v1" checked> <span class="sw v1"></span> Vendor 1</label>
  </div>

  <div class="footer">
    <span><kbd>Space</kbd> play / pause</span>
    <span>Data: visgl/deck.gl-data · Basemap: CARTO</span>
  </div>
</section>

<div id="camera-badge" class="panel"><span class="dot"></span><span id="camera-text">Camera orbiting</span></div>

<div id="loading">
  <div class="card">
    <div class="spinner"></div>
    <div class="msg" id="loading-msg">Loading 996 taxi trips and Manhattan buildings…</div>
  </div>
</div>

<script>
(function () {
  'use strict';

  // ------------------------------------------------------------------ config
  const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';
  const BUILDINGS_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/buildings.json';
  const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

  const INITIAL_VIEW_STATE = { longitude: -74, latitude: 40.72, zoom: 13, pitch: 45, bearing: 0 };

  const COLORS = { 0: [255, 176, 59], 1: [56, 214, 255] };
  const ORBIT_DEG_PER_SEC = 1.5;      // one full orbit every 4 minutes
  const RESUME_DELAY_MS = 2500;       // idle time before the camera drifts again

  const BUILDING_MATERIAL = { ambient: 0.18, diffuse: 0.65, shininess: 40, specularColor: [70, 76, 90] };

  // ------------------------------------------------------------------ state
  const state = {
    time: 0,
    speed: 60,
    trail: 180,
    playing: true,
    cinematic: true,
    showBuildings: true,
    vendors: { 0: true, 1: true },
    viewState: { ...INITIAL_VIEW_STATE },
    lastInteraction: performance.now(),
    fly: null
  };

  let trips = [];
  let buildings = null;
  let LOOP = 2500;
  let filteredCache = null;
  let filteredKey = '';

  // ------------------------------------------------------------------ helpers
  const $ = id => document.getElementById(id);
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const pad = n => String(n).padStart(2, '0');
  const fmtTime = s => { s = Math.max(0, Math.floor(s)); return pad(Math.floor(s / 60)) + ':' + pad(s % 60); };
  const easeInOut = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  function pathLengthKm(path) {
    let d = 0;
    for (let i = 1; i < path.length; i++) {
      const [lng1, lat1] = path[i - 1], [lng2, lat2] = path[i];
      const R = 6371, toR = Math.PI / 180;
      const dLat = (lat2 - lat1) * toR, dLng = (lng2 - lng1) * toR;
      const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * toR) * Math.cos(lat2 * toR) * Math.sin(dLng / 2) ** 2;
      d += 2 * R * Math.asin(Math.sqrt(a));
    }
    return d;
  }

  function filteredTrips() {
    const key = state.vendors[0] + '|' + state.vendors[1];
    if (key !== filteredKey) {
      filteredKey = key;
      filteredCache = trips.filter(t => state.vendors[t.vendor]);
    }
    return filteredCache;
  }

  // ------------------------------------------------------------------ lighting
  const lightingEffect = new deck.LightingEffect({
    ambient: new deck.AmbientLight({ color: [255, 255, 255], intensity: 1.0 }),
    key: new deck.PointLight({ color: [255, 245, 230], intensity: 2.0, position: [-74.05, 40.7, 8000] }),
    fill: new deck.PointLight({ color: [180, 210, 255], intensity: 1.0, position: [-73.5, 41.0, 8000] })
  });

  // ------------------------------------------------------------------ deck
  const deckgl = new deck.DeckGL({
    container: $('map'),
    mapLib: maplibregl,
    mapStyle: MAP_STYLE,
    viewState: state.viewState,
    controller: { minZoom: 10, maxZoom: 18, maxPitch: 70, inertia: true },
    effects: [lightingEffect],
    layers: [],
    useDevicePixels: true,
    onViewStateChange: ({ viewState }) => {
      state.viewState = viewState;
      state.fly = null;
      state.lastInteraction = performance.now();
      deckgl.setProps({ viewState });
    },
    getTooltip: ({ object }) => object && {
      html:
        '<div style="display:flex;align-items:center;gap:8px;font-weight:600;margin-bottom:6px">' +
          '<span style="width:10px;height:10px;border-radius:3px;background:rgb(' + COLORS[object.vendor].join(',') + ')"></span>' +
          'Vendor ' + object.vendor +
        '</div>' +
        '<div style="color:#a3adbf">Departs <b style="color:#e9edf4">' + fmtTime(object.timestamps[0]) + '</b></div>' +
        '<div style="color:#a3adbf">Duration <b style="color:#e9edf4">' + fmtTime(object._dur) + '</b></div>' +
        '<div style="color:#a3adbf">Distance <b style="color:#e9edf4">' + object._dist.toFixed(2) + ' km</b></div>' +
        '<div style="color:#a3adbf">' + object.path.length + ' GPS points</div>',
      style: {
        background: 'rgba(9,13,21,0.9)', color: '#e9edf4', fontSize: '12px', lineHeight: '1.5',
        borderRadius: '10px', padding: '10px 12px', border: '1px solid rgba(255,255,255,0.1)',
        fontFamily: 'Inter, system-ui, sans-serif', backdropFilter: 'blur(10px)'
      }
    }
  });

  // ------------------------------------------------------------------ layers
  function buildLayers() {
    const layers = [];
    if (state.showBuildings && buildings) {
      layers.push(new deck.PolygonLayer({
        id: 'buildings',
        data: buildings,
        extruded: true,
        wireframe: false,
        opacity: 1,
        getPolygon: d => d.polygon,
        getElevation: d => d.height,
        getFillColor: d => {
          const t = clamp((d.height || 0) / 250, 0, 1);
          return [36 + 34 * t, 44 + 38 * t, 58 + 46 * t];
        },
        material: BUILDING_MATERIAL
      }));
    }

    const data = filteredTrips();
    const common = {
      data,
      getPath: d => d.path,
      getTimestamps: d => d.timestamps,
      getColor: d => COLORS[d.vendor],
      capRounded: true,
      jointRounded: true,
      fadeTrail: true,
      currentTime: state.time
    };

    layers.push(new deck.TripsLayer({
      ...common,
      id: 'trips-glow',
      opacity: 0.14,
      widthMinPixels: 11,
      widthMaxPixels: 18,
      trailLength: state.trail * 0.55
    }));

    layers.push(new deck.TripsLayer({
      ...common,
      id: 'trips',
      opacity: 0.95,
      widthMinPixels: 2.5,
      widthMaxPixels: 6,
      trailLength: state.trail,
      pickable: true,
      autoHighlight: true,
      highlightColor: [255, 255, 255, 220]
    }));

    return layers;
  }

  // ------------------------------------------------------------------ HUD
  const el = {
    clock: $('clock'), active: $('active'), fill: $('bar-fill'), play: $('play'),
    badge: $('camera-badge'), badgeText: $('camera-text')
  };

  function updateHUD(now) {
    el.clock.textContent = fmtTime(state.time);
    el.fill.style.width = (100 * state.time / LOOP).toFixed(2) + '%';

    let active = 0;
    const data = filteredTrips();
    for (let i = 0; i < data.length; i++) {
      const ts = data[i].timestamps;
      if (ts[0] <= state.time && state.time <= ts[ts.length - 1]) active++;
    }
    el.active.textContent = active;

    const orbiting = state.cinematic && now - state.lastInteraction > RESUME_DELAY_MS && !state.fly;
    el.badge.classList.toggle('paused', !orbiting);
    el.badgeText.textContent = !state.cinematic ? 'Camera manual'
      : orbiting ? 'Camera orbiting' : 'Camera paused — resumes shortly';
  }

  // ------------------------------------------------------------------ animation
  let last = performance.now();

  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.1);
    last = now;

    if (state.playing) state.time = (state.time + dt * state.speed) % LOOP;

    if (state.fly) {
      const f = state.fly;
      const t = clamp((now - f.start) / f.duration, 0, 1);
      const k = easeInOut(t);
      let db = ((f.to.bearing - f.from.bearing + 540) % 360) - 180;
      state.viewState = {
        longitude: f.from.longitude + (f.to.longitude - f.from.longitude) * k,
        latitude: f.from.latitude + (f.to.latitude - f.from.latitude) * k,
        zoom: f.from.zoom + (f.to.zoom - f.from.zoom) * k,
        pitch: f.from.pitch + (f.to.pitch - f.from.pitch) * k,
        bearing: (f.from.bearing + db * k + 360) % 360
      };
      if (t >= 1) { state.fly = null; state.lastInteraction = now - RESUME_DELAY_MS; }
    } else if (state.cinematic && now - state.lastInteraction > RESUME_DELAY_MS) {
      const vs = state.viewState;
      state.viewState = {
        ...vs,
        bearing: (vs.bearing + dt * ORBIT_DEG_PER_SEC) % 360,
        pitch: clamp(vs.pitch + Math.sin(now / 18000) * dt * 0.7, 35, 60)
      };
    }

    deckgl.setProps({ viewState: state.viewState, layers: buildLayers() });
    updateHUD(now);
    requestAnimationFrame(frame);
  }

  // ------------------------------------------------------------------ UI wiring
  function setPlaying(p) {
    state.playing = p;
    el.play.textContent = p ? '❚❚' : '▶';
  }
  el.play.addEventListener('click', () => setPlaying(!state.playing));
  document.addEventListener('keydown', e => {
    if (e.code === 'Space' && !/INPUT|BUTTON/.test(e.target.tagName)) { e.preventDefault(); setPlaying(!state.playing); }
  });

  $('bar').addEventListener('click', e => {
    const r = e.currentTarget.getBoundingClientRect();
    state.time = clamp((e.clientX - r.left) / r.width, 0, 0.999) * LOOP;
  });

  $('speed').addEventListener('input', e => {
    state.speed = +e.target.value;
    $('speed-out').textContent = state.speed + '×';
  });
  $('trail').addEventListener('input', e => {
    state.trail = +e.target.value;
    $('trail-out').textContent = state.trail + ' s';
  });
  $('cinematic').addEventListener('change', e => {
    state.cinematic = e.target.checked;
    if (state.cinematic) state.lastInteraction = performance.now() - RESUME_DELAY_MS;
  });
  $('buildings').addEventListener('change', e => { state.showBuildings = e.target.checked; });
  $('v0').addEventListener('change', e => { state.vendors[0] = e.target.checked; });
  $('v1').addEventListener('change', e => { state.vendors[1] = e.target.checked; });

  $('reset').addEventListener('click', () => {
    state.fly = {
      from: { ...state.viewState },
      to: { ...INITIAL_VIEW_STATE },
      start: performance.now(),
      duration: 1400
    };
    state.lastInteraction = performance.now();
  });

  // ------------------------------------------------------------------ data
  function showError(message) {
    const m = $('loading-msg');
    m.classList.add('error');
    m.textContent = message;
    document.querySelector('.spinner').style.display = 'none';
  }

  Promise.all([
    fetch(DATA_URL).then(r => { if (!r.ok) throw new Error('Trips request failed (HTTP ' + r.status + ')'); return r.json(); }),
    fetch(BUILDINGS_URL).then(r => (r.ok ? r.json() : null)).catch(() => null)
  ]).then(([rawTrips, rawBuildings]) => {
    if (!Array.isArray(rawTrips) || rawTrips.length === 0) throw new Error('Trip dataset is empty or malformed.');

    trips = rawTrips.filter(d =>
      Array.isArray(d.path) && Array.isArray(d.timestamps) &&
      d.path.length >= 2 && d.path.length === d.timestamps.length &&
      (d.vendor === 0 || d.vendor === 1)
    );

    let maxT = 0, minT = Infinity, points = 0;
    for (const d of trips) {
      const ts = d.timestamps;
      minT = Math.min(minT, ts[0]);
      maxT = Math.max(maxT, ts[ts.length - 1]);
      points += d.path.length;
      d._dur = ts[ts.length - 1] - ts[0];
      d._dist = pathLengthKm(d.path);
    }
    LOOP = Math.ceil(maxT) + 30;

    buildings = Array.isArray(rawBuildings)
      ? rawBuildings.filter(b => Array.isArray(b.polygon) && typeof b.height === 'number')
      : null;
    if (!buildings) { $('buildings').checked = false; $('buildings').disabled = true; state.showBuildings = false; }

    $('stat-trips').textContent = trips.length.toLocaleString();
    $('stat-points').textContent = points.toLocaleString();
    $('stat-window').textContent = Math.round((maxT - minT) / 60) + ' min';
    $('loop-end').textContent = fmtTime(LOOP);

    state.lastInteraction = performance.now() - RESUME_DELAY_MS + 1500; // start drifting 1.5 s after load
    last = performance.now();
    requestAnimationFrame(frame);

    $('loading').classList.add('hidden');
  }).catch(err => {
    console.warn(err);
    showError('Could not load the trip data: ' + (err && err.message ? err.message : err) + '. Check your connection and reload.');
  });
})();
</script>
</body>
</html>
```