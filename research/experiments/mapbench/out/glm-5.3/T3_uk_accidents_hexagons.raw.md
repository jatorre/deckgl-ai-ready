```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>3D Hexagon Heatmap — GB Road Accidents</title>
<style>
  html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #111; }
  #deck-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
  #controls {
    position: absolute; top: 16px; left: 16px; z-index: 10;
    background: rgba(20, 22, 28, 0.9); color: #eee;
    padding: 14px 18px; border-radius: 8px;
    font-family: "Helvetica Neue", Arial, sans-serif; font-size: 13px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    user-select: none;
  }
  #controls label { display: block; margin-bottom: 6px; font-weight: 600; letter-spacing: 0.02em; }
  #controls .val { color: #ffb347; font-weight: 700; }
  input[type=range] { width: 240px; accent-color: #ffb347; }
  #loading {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    color: #fff; font-family: sans-serif; font-size: 16px; z-index: 20;
    background: rgba(0,0,0,0.6); padding: 12px 22px; border-radius: 6px;
  }
  #tooltip {
    position: absolute; z-index: 15; pointer-events: none; display: none;
    background: rgba(15, 17, 22, 0.92); color: #fff; padding: 6px 10px;
    border-radius: 4px; font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 12px; border: 1px solid rgba(255,255,255,0.15);
  }
</style>
</head>
<body>
<div id="loading">Loading accident data…</div>
<div id="controls">
  <label>Hexagon Radius: <span class="val" id="radius-val">1000</span> m</label>
  <input type="range" id="radius-slider" min="500" max="5000" step="50" value="1000">
</div>
<div id="tooltip"></div>
<canvas id="deck-canvas"></div>

<script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>

<script>
const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv';

const colorRange = [
  [1, 152, 189],   [73, 0, 146],   [0, 156, 99],
  [222, 47, 21],   [0, 0, 0],      [16, 149, 159],
  [2, 84, 133],    [121, 90, 71],  [1, 159, 159],
  [0, 0, 165],     [2, 190, 57],   [132, 238, 238]
];

let points = [];
let radius = 1000;

const deckgl = new deck.Deck({
  canvas: 'deck-canvas',
  views: new deck.MapView({ repeat: true }),
  initialViewState: {
    longitude: -1.4157,
    latitude: 52.2324,
    zoom: 6.6,
    pitch: 45,
    bearing: -27
  },
  controller: true,
  getTooltip: null,
  layers: [
    basemapLayer(),
    hexagonLayer(1000)
  ]
});

const tooltipEl = document.getElementById('tooltip');

function basemapLayer() {
  return new deck.TileLayer({
    id: 'basemap',
    data: 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
    minZoom: 0,
    maxZoom: 19,
    tileSize: 512,
    renderSubLayers: props => {
      const { bbox: { west, south, east, north } } = props;
      return new deck.BitmapLayer(props, {
        data: null,
        image: props.data,
        bounds: [west, south, east, north]
      });
    },
    pickable: false
  });
}

function hexagonLayer(r) {
  return new deck.HexagonLayer({
    id: 'accidents',
    data: points,
    getPosition: d => d,
    radius: r,
    elevationScale: 60,
    extruded: true,
    pickable: true,
    onHover: onHover,
    opacity: 1,
    colorRange: colorRange,
    elevationRange: [0, 3000],
    elevationDomain: null,
    colorDomain: null,
    coverage: 1,
    material: {
      ambient: 0.64,
      diffuse: 0.6,
      shininess: 32,
      specularColor: [51, 51, 51]
    },
    transitions: { radius: 300 }
  });
}

function onHover(info, event) {
  if (info.object && info.object.points) {
    const count = info.object.points.length;
    tooltipEl.style.display = 'block';
    tooltipEl.innerHTML = '<b>Accidents in cell:</b> ' + count.toLocaleString();
    tooltipEl.style.left = (event.x + 14) + 'px';
    tooltipEl.style.top = (event.y + 14) + 'px';
  } else {
    tooltipEl.style.display = 'none';
  }
}

function updateLayers() {
  deckgl.setProps({ layers: [basemapLayer(), hexagonLayer(radius)] });
}

const slider = document.getElementById('radius-slider');
const radiusVal = document.getElementById('radius-val');
slider.addEventListener('input', () => {
  radius = parseInt(slider.value, 10);
  radiusVal.textContent = radius;
  updateLayers();
});

// Load real data
fetch(DATA_URL)
  .then(res => res.text())
  .then(text => {
    const lines = text.split('\n');
    points = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      const parts = line.split(',');
      const lng = parseFloat(parts[0]);
      const lat = parseFloat(parts[1]);
      if (isFinite(lng) && isFinite(lat)) points.push([lng, lat]);
    }
    document.getElementById('loading').style.display = 'none';
    updateLayers();
  })
  .catch(err => {
    document.getElementById('loading').textContent = 'Failed to load data: ' + err;
  });
</script>
</body>
</html>
```