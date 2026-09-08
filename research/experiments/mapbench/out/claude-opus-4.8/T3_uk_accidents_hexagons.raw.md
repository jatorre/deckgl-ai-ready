```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Deck.gl 3D Hexagon Heatmap</title>
<script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
<script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
<link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
<script src="https://unpkg.com/papaparse@5.4.1/papaparse.min.js"></script>
<style>
  html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
  #map { position: absolute; width: 100%; height: 100%; }
  #controls {
    position: absolute; top: 12px; left: 12px; z-index: 10;
    background: rgba(30,30,30,0.85); color: #fff; padding: 12px 16px;
    border-radius: 8px; font-family: sans-serif; font-size: 13px;
  }
  #controls label { display: block; margin-bottom: 6px; }
  #radius { width: 200px; }
  #tooltip {
    position: absolute; z-index: 20; pointer-events: none;
    background: rgba(0,0,0,0.8); color: #fff; padding: 6px 10px;
    border-radius: 4px; font-family: sans-serif; font-size: 12px; display: none;
  }
</style>
</head>
<body>
<div id="map"></div>
<div id="controls">
  <label>Hexagon radius: <span id="radiusValue">1000</span> m</label>
  <input id="radius" type="range" min="500" max="5000" step="100" value="1000" />
</div>
<div id="tooltip"></div>
<script>
const {DeckGL, HexagonLayer} = deck;

const INITIAL_VIEW_STATE = {
  longitude: -1.4157,
  latitude: 52.2324,
  zoom: 6.6,
  pitch: 45,
  bearing: -27
};

const COLOR_RANGE = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];

const lightingEffect = new deck.LightingEffect({
  ambientLight: new deck.AmbientLight({color: [255, 255, 255], intensity: 1.0}),
  directionalLight1: new deck.DirectionalLight({
    color: [255, 255, 255], intensity: 1.0, direction: [-3, -9, -1]
  }),
  pointLight: new deck.PointLight({
    color: [255, 255, 255], intensity: 0.8, position: [-1.4157, 52.2324, 8000]
  })
});

let data = [];
let radius = 1000;
const tooltip = document.getElementById('tooltip');

function makeLayer() {
  return new HexagonLayer({
    id: 'hexagon-layer',
    data,
    getPosition: d => d,
    radius,
    elevationScale: 50,
    extruded: true,
    pickable: true,
    colorRange: COLOR_RANGE,
    coverage: 1,
    material: {
      ambient: 0.64,
      diffuse: 0.6,
      shininess: 32,
      specularColor: [51, 51, 51]
    }
  });
}

const deckgl = new DeckGL({
  container: 'map',
  mapLib: maplibregl,
  mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  initialViewState: INITIAL_VIEW_STATE,
  controller: true,
  effects: [lightingEffect],
  layers: [],
  getTooltip: null,
  onHover: info => {
    if (info.object && info.object.points) {
      tooltip.style.display = 'block';
      tooltip.style.left = info.x + 12 + 'px';
      tooltip.style.top = info.y + 12 + 'px';
      tooltip.innerHTML = 'Count: ' + info.object.points.length;
    } else {
      tooltip.style.display = 'none';
    }
  }
});

function render() {
  deckgl.setProps({layers: [makeLayer()]});
}

const slider = document.getElementById('radius');
const radiusValue = document.getElementById('radiusValue');
slider.addEventListener('input', e => {
  radius = Number(e.target.value);
  radiusValue.textContent = radius;
  render();
});

Papa.parse('https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv', {
  download: true,
  header: true,
  dynamicTyping: true,
  complete: results => {
    data = results.data
      .filter(d => d.lng != null && d.lat != null && !isNaN(d.lng) && !isNaN(d.lat))
      .map(d => [d.lng, d.lat]);
    render();
  }
});
</script>
</body>
</html>
```