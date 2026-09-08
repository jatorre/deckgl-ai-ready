```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Deck.gl Trips Animation</title>
  <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  <style>
    html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
    #map { position: absolute; width: 100%; height: 100%; }
    #controls {
      position: absolute; top: 10px; left: 10px; z-index: 10;
      background: rgba(0,0,0,0.7); color: #fff; padding: 10px 14px;
      border-radius: 6px; font-family: sans-serif; font-size: 14px;
    }
    #controls button {
      background: #444; color: #fff; border: none; padding: 6px 12px;
      border-radius: 4px; cursor: pointer; font-size: 14px; margin-right: 10px;
    }
    #controls button:hover { background: #666; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="controls">
    <button id="playPause">Pause</button>
    <span id="timeReadout">Time: 0 s</span>
  </div>
  <script>
    const {DeckGL, TripsLayer} = deck;

    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json';

    const LOOP_LENGTH = 2487;    // data time span (seconds)
    const TRAIL_LENGTH = 180;    // trail length in seconds
    const ANIMATION_SPEED = LOOP_LENGTH / 60; // one full pass in ~60 real seconds

    let currentTime = 0;
    let playing = true;
    let lastTimestamp = null;
    let tripsData = null;

    const deckgl = new DeckGL({
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
      controller: true
    });

    function renderLayers() {
      const layers = [
        new TripsLayer({
          id: 'trips',
          data: tripsData,
          getPath: d => d.path,
          getTimestamps: d => d.timestamps,
          getColor: d => d.vendor === 0 ? [253, 128, 93] : [23, 184, 190],
          opacity: 0.8,
          widthMinPixels: 3,
          rounded: true,
          trailLength: TRAIL_LENGTH,
          currentTime: currentTime,
          shadowEnabled: false
        })
      ];
      deckgl.setProps({layers});
    }

    function animate(timestamp) {
      if (playing && tripsData) {
        if (lastTimestamp !== null) {
          const delta = (timestamp - lastTimestamp) / 1000; // seconds elapsed
          currentTime = (currentTime + delta * ANIMATION_SPEED) % LOOP_LENGTH;
        }
        document.getElementById('timeReadout').textContent =
          'Time: ' + currentTime.toFixed(0) + ' s';
        renderLayers();
      }
      lastTimestamp = timestamp;
      requestAnimationFrame(animate);
    }

    document.getElementById('playPause').addEventListener('click', () => {
      playing = !playing;
      document.getElementById('playPause').textContent = playing ? 'Pause' : 'Play';
    });

    fetch(DATA_URL)
      .then(res => res.json())
      .then(data => {
        tripsData = data;
        renderLayers();
        requestAnimationFrame(animate);
      });
  </script>
</body>
</html>
```