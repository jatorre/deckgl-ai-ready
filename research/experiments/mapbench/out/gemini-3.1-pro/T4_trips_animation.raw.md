```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>deck.gl TripsLayer with MapLibre</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: #000;
      font-family: sans-serif;
    }
    #map {
      width: 100vw;
      height: 100vh;
      position: absolute;
      top: 0;
      left: 0;
    }
    #control-panel {
      position: absolute;
      top: 20px;
      left: 20px;
      z-index: 10;
      background: rgba(20, 20, 20, 0.85);
      color: #fff;
      padding: 15px;
      border-radius: 6px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.5);
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 150px;
    }
    #time-readout {
      font-size: 16px;
      font-weight: bold;
    }
    button {
      background: #444;
      color: #fff;
      border: 1px solid #666;
      padding: 8px;
      cursor: pointer;
      border-radius: 4px;
      font-size: 14px;
      transition: background 0.2s;
    }
    button:hover {
      background: #555;
    }
  </style>

  <script src="https://unpkg.com/maplibre-gl@3.3.1/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.3.1/dist/maplibre-gl.css" rel="stylesheet" />
  <script>
    window.mapboxgl = maplibregl;
  </script>
  <script src="https://unpkg.com/deck.gl@8.9.0/dist.min.js"></script>
</head>
<body>

  <div id="map"></div>
  
  <div id="control-panel">
    <div id="time-readout">Time: 0s</div>
    <button id="play-pause-btn">Pause</button>
  </div>

  <script>
    const LOOP_LENGTH = 2500; 
    const REAL_SECONDS_PER_LOOP = 60;
    const ANIMATION_SPEED = LOOP_LENGTH / REAL_SECONDS_PER_LOOP; 
    
    let time = 0;
    let isPlaying = true;
    let lastTime = performance.now();
    let animationFrame;

    const deckgl = new deck.DeckGL({
      container: 'map',
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

    function renderLayers() {
      const tripsLayer = new deck.TripsLayer({
        id: 'trips',
        data: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json',
        getPath: d => d.path,
        getTimestamps: d => d.timestamps,
        getColor: d => d.vendor === 0 ? [253, 128, 93] : [23, 184, 190],
        opacity: 0.8,
        widthMinPixels: 3,
        trailLength: 180,
        currentTime: time
      });

      deckgl.setProps({
        layers: [tripsLayer]
      });
    }

    function animate(currentTimeMs) {
      if (isPlaying) {
        const dt = (currentTimeMs - lastTime) / 1000;
        time = (time + dt * ANIMATION_SPEED) % LOOP_LENGTH;
        document.getElementById('time-readout').innerText = `Time: ${Math.floor(time)}s`;
        renderLayers();
      }
      lastTime = currentTimeMs;
      animationFrame = requestAnimationFrame(animate);
    }

    document.getElementById('play-pause-btn').addEventListener('click', () => {
      isPlaying = !isPlaying;
      document.getElementById('play-pause-btn').innerText = isPlaying ? 'Pause' : 'Play';
      if (isPlaying) {
        lastTime = performance.now();
      }
    });

    animationFrame = requestAnimationFrame(animate);
  </script>

</body>
</html>
```