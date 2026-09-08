```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GB Road Accidents – 3D Hexagon Heatmap</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css">
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
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
      background: rgba(20, 20, 20, 0.85);
      color: #eee;
      padding: 12px 14px;
      border-radius: 6px;
      font-size: 13px;
      min-width: 240px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    #controls h1 {
      font-size: 14px;
      margin: 0 0 8px 0;
      font-weight: 600;
    }
    #controls label {
      display: block;
      margin-bottom: 4px;
    }
    #controls input[type=range] {
      width: 100%;
    }
    #status {
      margin-top: 8px;
      color: #aaa;
      font-size: 12px;
    }
    #legend {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: #ccc;
    }
    #legend .bar {
      flex: 1;
      height: 10px;
      background: linear-gradient(to right,
        rgb(1,152,189), rgb(73,227,206), rgb(216,254,181),
        rgb(254,237,177), rgb(254,173,84), rgb(209,55,78));
      border-radius: 2px;
    }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="controls">
    <h1>GB Road Accidents – 3D Hexagons</h1>
    <label for="radius">Hexagon radius: <strong id="radiusValue">1000</strong> m</label>
    <input id="radius" type="range" min="500" max="5000" step="100" value="1000">
    <div id="legend"><span>Low</span><div class="bar"></div><span>High</span></div>
    <div id="status">Loading data…</div>
  </div>

  <script>
    const {DeckGL, HexagonLayer, AmbientLight, PointLight, LightingEffect} = deck;

    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv';
    const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

    const INITIAL_VIEW_STATE = {
      longitude: -1.4157,
      latitude: 52.2324,
      zoom: 6.6,
      pitch: 45,
      bearing: -27,
      minZoom: 3,
      maxZoom: 16
    };

    const COLOR_RANGE = [
      [1, 152, 189],
      [73, 227, 206],
      [216, 254, 181],
      [254, 237, 177],
      [254, 173, 84],
      [209, 55, 78]
    ];

    const ambientLight = new AmbientLight({
      color: [255, 255, 255],
      intensity: 1.0
    });
    const pointLight1 = new PointLight({
      color: [255, 255, 255],
      intensity: 0.8,
      position: [-0.144528, 49.739968, 80000]
    });
    const pointLight2 = new PointLight({
      color: [255, 255, 255],
      intensity: 0.8,
      position: [-3.807751, 54.104682, 8000]
    });
    const lightingEffect = new LightingEffect({ambientLight, pointLight1, pointLight2});

    const material = {
      ambient: 0.64,
      diffuse: 0.6,
      shininess: 32,
      specularColor: [51, 51, 51]
    };

    let data = [];
    let radius = 1000;

    function buildLayer() {
      return new HexagonLayer({
        id: 'hexagons',
        data,
        radius,
        coverage: 1,
        extruded: true,
        pickable: true,
        elevationRange: [0, 3000],
        elevationScale: data.length ? 50 : 0,
        colorRange: COLOR_RANGE,
        material,
        getPosition: d => d,
        upperPercentile: 100,
        transitions: {
          elevationScale: 1000
        }
      });
    }

    const deckgl = new DeckGL({
      container: 'map',
      mapLib: maplibregl,
      mapStyle: MAP_STYLE,
      initialViewState: INITIAL_VIEW_STATE,
      controller: true,
      effects: [lightingEffect],
      layers: [buildLayer()],
      getTooltip: ({object}) => {
        if (!object) return null;
        const count = object.count !== undefined
          ? object.count
          : (object.points ? object.points.length : 0);
        const pos = object.position || [];
        const lng = pos[0] !== undefined ? pos[0].toFixed(4) : '';
        const lat = pos[1] !== undefined ? pos[1].toFixed(4) : '';
        return {
          html: `<div style="font-size:13px"><strong>${count.toLocaleString()}</strong> accident${count === 1 ? '' : 's'}<br>
                 <span style="color:#bbb;font-size:11px">${lat}, ${lng}</span></div>`,
          style: {
            background: 'rgba(20,20,20,0.9)',
            color: '#fff',
            padding: '6px 10px',
            borderRadius: '4px',
            fontFamily: 'sans-serif'
          }
        };
      }
    });

    function render() {
      deckgl.setProps({layers: [buildLayer()]});
    }

    const slider = document.getElementById('radius');
    const radiusValue = document.getElementById('radiusValue');
    slider.addEventListener('input', e => {
      radius = Number(e.target.value);
      radiusValue.textContent = radius;
      render();
    });

    function parseCSV(text) {
      const lines = text.split(/\r?\n/);
      const out = [];
      let start = 0;
      if (lines.length && /lng|lat/i.test(lines[0])) start = 1;
      for (let i = start; i < lines.length; i++) {
        const line = lines[i];
        if (!line) continue;
        const idx = line.indexOf(',');
        if (idx < 0) continue;
        const lng = Number(line.slice(0, idx));
        const lat = Number(line.slice(idx + 1));
        if (Number.isFinite(lng) && Number.isFinite(lat)) out.push([lng, lat]);
      }
      return out;
    }

    const status = document.getElementById('status');
    fetch(DATA_URL)
      .then(r => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      })
      .then(text => {
        data = parseCSV(text);
        status.textContent = data.length.toLocaleString() + ' accident locations loaded. Drag to rotate, scroll to zoom.';
        render();
      })
      .catch(err => {
        status.textContent = 'Failed to load data: ' + err.message;
        console.error(err);
      });
  </script>
</body>
</html>
```