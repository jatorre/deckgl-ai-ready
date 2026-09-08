```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>NYC Taxi Trips — deck.gl TripsLayer</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
  <script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@9.0.35/dist.min.js"></script>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #000;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #map {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    #controls {
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 10;
      background: rgba(20, 20, 24, 0.85);
      color: #eee;
      padding: 10px 14px;
      border-radius: 6px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      user-select: none;
    }
    #playPause {
      background: #2b7cff;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 6px 14px;
      font-size: 14px;
      cursor: pointer;
      min-width: 72px;
    }
    #playPause:hover { background: #4a8fff; }
    #timeReadout {
      font-variant-numeric: tabular-nums;
      min-width: 150px;
    }
    #legend {
      display: flex;
      gap: 10px;
      align-items: center;
      padding-left: 12px;
      border-left: 1px solid rgba(255,255,255,0.2);
    }
    .swatch {
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 2px;
      margin-right: 5px;
      vertical-align: middle;
    }
    #status {
      position: absolute;
      bottom: 12px;
      left: 12px;
      z-index: 10;
      color: #bbb;
      font-size: 12px;
      background: rgba(20,20,24,0.7);
      padding: 4px 8px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <div id="controls">
    <button id="playPause">Pause</button>
    <div id="timeReadout">Time: 0 s</div>
    <div id="legend">
      <span><span class="swatch" style="background: rgb(253,128,93)"></span>Vendor 0</span>
      <span><span class="swatch" style="background: rgb(23,184,190)"></span>Vendor 1</span>
    </div>
  </div>
  <div id="status">Loading trips…</div>

  <script>
    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';
    const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

    const INITIAL_VIEW_STATE = {
      longitude: -74.00,
      latitude: 40.72,
      zoom: 12,
      pitch: 45,
      bearing: 0
    };

    const TRAIL_LENGTH = 180;       // seconds of trail
    const LOOP_LENGTH = 2500;       // data spans ~6 to ~2487 s
    const LOOP_REAL_SECONDS = 60;   // one full pass in ~60 real seconds
    const SPEED = LOOP_LENGTH / LOOP_REAL_SECONDS; // data seconds per real second

    const VENDOR_COLORS = {
      0: [253, 128, 93],
      1: [23, 184, 190]
    };

    let trips = null;
    let currentTime = 0;
    let playing = true;
    let lastFrame = null;

    const readout = document.getElementById('timeReadout');
    const status = document.getElementById('status');
    const btn = document.getElementById('playPause');

    const deckgl = new deck.DeckGL({
      container: 'map',
      mapLib: maplibregl,
      mapStyle: MAP_STYLE,
      initialViewState: INITIAL_VIEW_STATE,
      controller: true,
      layers: []
    });

    function buildLayers() {
      if (!trips) return [];
      return [
        new deck.TripsLayer({
          id: 'trips',
          data: trips,
          getPath: d => d.path,
          getTimestamps: d => d.timestamps,
          getColor: d => VENDOR_COLORS[d.vendor] || [255, 255, 255],
          opacity: 0.8,
          widthMinPixels: 2,
          rounded: true,
          capRounded: true,
          jointRounded: true,
          fadeTrail: true,
          trailLength: TRAIL_LENGTH,
          currentTime: currentTime,
          shadowEnabled: false
        })
      ];
    }

    function render() {
      deckgl.setProps({ layers: buildLayers() });
      readout.textContent = 'Time: ' + Math.floor(currentTime) + ' s';
    }

    function animate(ts) {
      if (lastFrame === null) lastFrame = ts;
      const dt = (ts - lastFrame) / 1000;
      lastFrame = ts;
      if (playing && trips) {
        currentTime = (currentTime + dt * SPEED) % LOOP_LENGTH;
        render();
      }
      requestAnimationFrame(animate);
    }

    btn.addEventListener('click', () => {
      playing = !playing;
      btn.textContent = playing ? 'Pause' : 'Play';
    });

    fetch(DATA_URL)
      .then(r => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(json => {
        trips = json;
        status.textContent = trips.length + ' trips loaded';
        render();
        requestAnimationFrame(animate);
      })
      .catch(err => {
        status.textContent = 'Failed to load data: ' + err.message;
        console.error(err);
      });
  </script>
</body>
</html>
```