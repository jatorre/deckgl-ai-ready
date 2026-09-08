```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Animated NYC Trips</title>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css">
  <style>
    html, body, #map {
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
    }
    body {
      background: #10151c;
      color: #f1f5f9;
      font-family: system-ui, sans-serif;
    }
    #controls {
      position: absolute;
      z-index: 10;
      top: 16px;
      left: 16px;
      max-width: calc(100vw - 64px);
      padding: 16px;
      background: rgba(15, 23, 35, 0.94);
      border: 1px solid #334155;
      border-radius: 10px;
      box-shadow: 0 6px 24px #0005;
    }
    h1 {
      margin: 0 0 12px;
      font-size: 18px;
    }
    .row {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }
    button {
      min-width: 76px;
      padding: 8px 14px;
      border: 1px solid #64748b;
      border-radius: 6px;
      background: #25354a;
      color: white;
      cursor: pointer;
      font: inherit;
    }
    button:hover:not(:disabled) { background: #354b67; }
    button:focus-visible { outline: 2px solid #38d9ff; outline-offset: 3px; }
    button:disabled { opacity: 0.5; cursor: wait; }
    #time { font-variant-numeric: tabular-nums; }
    .legend {
      display: flex;
      gap: 18px;
      margin-top: 14px;
      font-size: 13px;
    }
    .swatch {
      display: inline-block;
      width: 18px;
      height: 4px;
      margin-right: 6px;
      vertical-align: middle;
      border-radius: 2px;
    }
    #status {
      max-width: 290px;
      margin: 12px 0 0;
      color: #b8c5d5;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div id="map" aria-label="Animated map of New York City trips"></div>
  <section id="controls" aria-label="Trip animation controls">
    <h1>NYC Trip Trails</h1>
    <div class="row">
      <button id="toggle" type="button" disabled>Pause</button>
      <span>Time: <output id="time">6.0</output> s</span>
    </div>
    <div class="legend">
      <span><i class="swatch" style="background:#38d9ff"></i>Vendor 0</span>
      <span><i class="swatch" style="background:#ff9850"></i>Vendor 1</span>
    </div>
    <p id="status" role="status">Loading real trip data…</p>
  </section>

  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.36/dist.min.js"></script>
  <script>
    (() => {
      'use strict';

      const DATA_URL =
        'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';
      const COLORS = [[56, 217, 255], [255, 152, 80]];
      const LOOP_DURATION_MS = 60000;
      const TRAIL_LENGTH = 180;

      const button = document.getElementById('toggle');
      const timeOutput = document.getElementById('time');
      const status = document.getElementById('status');

      const map = new deck.DeckGL({
        container: 'map',
        mapLib: maplibregl,
        mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
        initialViewState: {
          longitude: -74.00,
          latitude: 40.72,
          zoom: 12,
          pitch: 45,
          bearing: 0
        },
        controller: true,
        layers: []
      });

      let trips;
      let minTime;
      let maxTime;
      let elapsedMs = 0;
      let playing = true;
      let previousFrame = null;

      function renderTrips(currentTime) {
        map.setProps({
          layers: [
            new deck.TripsLayer({
              id: 'trip-trails',
              data: trips,
              getPath: trip => trip.path,
              getTimestamps: trip => trip.timestamps,
              getColor: trip => COLORS[trip.vendor],
              currentTime,
              trailLength: TRAIL_LENGTH,
              fadeTrail: true,
              opacity: 0.9,
              widthMinPixels: 3,
              capRounded: true,
              jointRounded: true,
              pickable: false
            })
          ]
        });
        timeOutput.textContent = currentTime.toFixed(1);
      }

      function advance(now) {
        if (playing && previousFrame !== null) {
          elapsedMs = (elapsedMs + now - previousFrame) % LOOP_DURATION_MS;
        }
        previousFrame = now;
      }

      function animate(now) {
        advance(now);
        if (playing) {
          const currentTime =
            minTime + (elapsedMs / LOOP_DURATION_MS) * (maxTime - minTime);
          renderTrips(currentTime);
        }
        requestAnimationFrame(animate);
      }

      button.addEventListener('click', () => {
        advance(performance.now());
        playing = !playing;
        button.textContent = playing ? 'Pause' : 'Play';
        renderTrips(minTime + (elapsedMs / LOOP_DURATION_MS) * (maxTime - minTime));
      });

      async function loadTrips() {
        try {
          const response = await fetch(DATA_URL);
          if (!response.ok) {
            throw new Error('Dataset request failed: HTTP ' + response.status);
          }

          trips = await response.json();
          if (!Array.isArray(trips) || trips.length === 0) {
            throw new Error('The dataset contains no trips.');
          }

          minTime = Infinity;
          maxTime = -Infinity;
          for (const trip of trips) {
            for (const timestamp of trip.timestamps) {
              if (Number.isFinite(timestamp)) {
                minTime = Math.min(minTime, timestamp);
                maxTime = Math.max(maxTime, timestamp);
              }
            }
          }

          if (!Number.isFinite(minTime) || maxTime <= minTime) {
            throw new Error('The dataset has an invalid timestamp range.');
          }

          renderTrips(minTime);
          status.textContent =
            trips.length.toLocaleString() +
            ' trips · 180 s trails · 60 s per loop';
          button.disabled = false;
          requestAnimationFrame(animate);
        } catch (error) {
          console.error(error);
          status.textContent = 'Unable to load trips. ' + error.message;
          button.disabled = true;
        }
      }

      loadTrips();
    })();
  </script>
</body>
</html>
```