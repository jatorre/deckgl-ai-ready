```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NYC Animated Trips</title>

  <link
    rel="stylesheet"
    href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css"
  >

  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.36/dist.min.js"></script>

  <style>
    html,
    body,
    #map {
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
    }

    body {
      background: #111;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    #controls {
      position: absolute;
      top: 16px;
      left: 16px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      color: #fff;
      background: rgba(15, 18, 22, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 6px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(6px);
    }

    #playPause {
      min-width: 72px;
      padding: 7px 12px;
      color: #fff;
      background: #276ef1;
      border: 0;
      border-radius: 4px;
      font: inherit;
      font-weight: 600;
      cursor: pointer;
    }

    #playPause:hover:not(:disabled) {
      background: #3d7df3;
    }

    #playPause:disabled {
      opacity: 0.55;
      cursor: wait;
    }

    #time {
      min-width: 112px;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <div id="controls">
    <button id="playPause" type="button" disabled>Loading…</button>
    <span id="time">Time: —</span>
  </div>

  <script>
    const DATA_URL =
      "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json";

    const map = new maplibregl.Map({
      container: "map",
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [-74.00, 40.72],
      zoom: 12,
      pitch: 45,
      bearing: 0,
      antialias: true
    });

    const overlay = new deck.MapboxOverlay({
      interleaved: true,
      layers: []
    });

    map.addControl(overlay);

    const button = document.getElementById("playPause");
    const timeReadout = document.getElementById("time");

    let trips = [];
    let minTime = 0;
    let maxTime = 1;
    let currentTime = 0;
    let playing = true;
    let previousFrame = performance.now();

    function createTripsLayer() {
      return new deck.TripsLayer({
        id: "trips",
        data: trips,
        getPath: trip => trip.path,
        getTimestamps: trip => trip.timestamps,
        getColor: trip =>
          trip.vendor === 0 ? [0, 200, 255] : [255, 90, 40],
        opacity: 0.9,
        widthMinPixels: 2,
        widthMaxPixels: 5,
        rounded: true,
        fadeTrail: true,
        trailLength: 180,
        currentTime
      });
    }

    function renderLayer() {
      overlay.setProps({
        layers: [createTripsLayer()]
      });
      timeReadout.textContent = `Time: ${currentTime.toFixed(1)} s`;
    }

    function animate(now) {
      if (playing && trips.length) {
        const elapsedMilliseconds = now - previousFrame;
        const dataDuration = maxTime - minTime;

        currentTime += elapsedMilliseconds * dataDuration / 60000;

        if (currentTime >= maxTime) {
          currentTime =
            minTime + ((currentTime - minTime) % dataDuration);
        }

        renderLayer();
      }

      previousFrame = now;
      requestAnimationFrame(animate);
    }

    button.addEventListener("click", () => {
      playing = !playing;
      button.textContent = playing ? "Pause" : "Play";
      previousFrame = performance.now();
    });

    fetch(DATA_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        trips = data;

        const timestamps = trips.flatMap(trip => trip.timestamps);
        minTime = Math.min(...timestamps);
        maxTime = Math.max(...timestamps);
        currentTime = minTime;

        button.disabled = false;
        button.textContent = "Pause";
        renderLayer();
        previousFrame = performance.now();
        requestAnimationFrame(animate);
      })
      .catch(error => {
        console.error(error);
        button.textContent = "Error";
        timeReadout.textContent = "Failed to load data";
      });
  </script>
</body>
</html>
```