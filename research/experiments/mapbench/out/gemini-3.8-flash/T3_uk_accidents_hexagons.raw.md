```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Great Britain Road Accidents - deck.gl 3D Heatmap</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- MapLibre GL CSS & JS -->
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>

  <!-- deck.gl standalone -->
  <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>

  <!-- PapaParse for fast CSV parsing -->
  <script src="https://unpkg.com/papaparse@5.4.1/papaparse.min.js"></script>

  <style>
    * {
      box-sizing: border-box;
    }
    body, html {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #111;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #map-container {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
    }
    .control-panel {
      position: absolute;
      top: 20px;
      left: 20px;
      z-index: 10;
      background: rgba(18, 18, 24, 0.85);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 18px 20px;
      color: #f3f3f3;
      width: 300px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .panel-title {
      margin: 0 0 6px 0;
      font-size: 16px;
      font-weight: 600;
      letter-spacing: 0.3px;
    }
    .panel-subtitle {
      margin: 0 0 16px 0;
      font-size: 12px;
      color: #9da3af;
      line-height: 1.4;
    }
    .control-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      font-size: 13px;
    }
    .control-label {
      font-weight: 500;
    }
    .control-value {
      font-weight: 600;
      font-variant-numeric: tabular-nums;
      color: #49e3ce;
    }
    input[type=range] {
      width: 100%;
      margin: 4px 0 16px 0;
      -webkit-appearance: none;
      background: #2c2f38;
      height: 6px;
      border-radius: 3px;
      outline: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #49e3ce;
      cursor: pointer;
      box-shadow: 0 0 4px rgba(0,0,0,0.5);
    }
    input[type=range]::-moz-range-thumb {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #49e3ce;
      cursor: pointer;
      border: none;
    }
    .legend-bar {
      height: 8px;
      border-radius: 4px;
      background: linear-gradient(to right, rgb(1,152,189), rgb(73,227,206), rgb(216,254,181), rgb(254,237,177), rgb(254,173,84), rgb(209,55,78));
      margin-bottom: 6px;
    }
    .legend-labels {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #8c93a0;
    }
    #loader {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 20;
      background: rgba(18, 18, 24, 0.9);
      padding: 18px 26px;
      border-radius: 8px;
      color: #f3f3f3;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .spinner {
      width: 20px;
      height: 20px;
      border: 3px solid rgba(255, 255, 255, 0.2);
      border-top-color: #49e3ce;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div id="map-container"></div>

  <div class="control-panel">
    <h3 class="panel-title">GB Road Accidents</h3>
    <p class="panel-subtitle">Aggregated 3D hexagon visualization of accident frequency across Great Britain.</p>
    
    <div class="control-row">
      <span class="control-label">Hexagon Radius</span>
      <span id="radius-val" class="control-value">1,000 m</span>
    </div>
    <input type="range" id="radius-slider" min="500" max="5000" step="100" value="1000">

    <div class="control-row" style="margin-top: 4px;">
      <span class="control-label">Accident Density</span>
    </div>
    <div class="legend-bar"></div>
    <div class="legend-labels">
      <span>Fewer</span>
      <span>More</span>
    </div>
  </div>

  <div id="loader">
    <div class="spinner"></div>
    <span id="loader-text">Loading 140,000 accident records...</span>
  </div>

  <script>
    const INITIAL_VIEW_STATE = {
      longitude: -1.4157,
      latitude: 52.2324,
      zoom: 6.6,
      pitch: 45,
      bearing: -27,
      maxZoom: 20,
      minZoom: 4
    };

    const colorRange = [
      [1, 152, 189],
      [73, 227, 206],
      [216, 254, 181],
      [254, 237, 177],
      [254, 173, 84],
      [209, 55, 78]
    ];

    const ambientLight = new deck.AmbientLight({
      color: [255, 255, 255],
      intensity: 1.0
    });

    const pointLight1 = new deck.PointLight({
      color: [255, 255, 255],
      intensity: 0.8,
      position: [-0.144528, 49.739968, 80000]
    });

    const pointLight2 = new deck.PointLight({
      color: [255, 255, 255],
      intensity: 0.8,
      position: [-3.807751, 54.104682, 80000]
    });

    const lightingEffect = new deck.LightingEffect({ ambientLight, pointLight1, pointLight2 });

    const material = {
      ambient: 0.64,
      diffuse: 0.6,
      shininess: 32,
      specularColor: [51, 51, 51]
    };

    let accidentData = [];
    let currentRadius = 1000;

    const deckgl = new deck.DeckGL({
      container: 'map-container',
      mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
      initialViewState: INITIAL_VIEW_STATE,
      controller: true,
      effects: [lightingEffect],
      getTooltip: ({ object }) => {
        if (!object) return null;
        const count = object.count || (object.points && object.points.length) || 0;
        const [lng, lat] = object.position;
        return {
          html: `
            <div style="font-weight: 600; margin-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 2px;">Hexagon Bin</div>
            <div><b>Accidents:</b> ${count.toLocaleString()}</div>
            <div style="color: #aaa; font-size: 11px; margin-top: 2px;">Approx. ${lat.toFixed(3)}°N, ${lng.toFixed(3)}°E</div>
          `,
          style: {
            backgroundColor: 'rgba(20, 20, 25, 0.95)',
            color: '#fff',
            fontSize: '12px',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            padding: '8px 12px',
            borderRadius: '6px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
            border: '1px solid rgba(255,255,255,0.1)'
          }
        };
      }
    });

    function renderLayers() {
      const hexagonLayer = new deck.HexagonLayer({
        id: 'heatmap',
        data: accidentData,
        getPosition: d => [d[0], d[1]],
        radius: currentRadius,
        elevationRange: [0, 3000],
        elevationScale: 50,
        extruded: true,
        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 255, 120],
        colorRange: colorRange,
        material: material,
        coverage: 0.95,
        updateTriggers: {
          radius: currentRadius
        }
      });

      deckgl.setProps({
        layers: [hexagonLayer]
      });
    }

    const slider = document.getElementById('radius-slider');
    const radiusVal = document.getElementById('radius-val');

    slider.addEventListener('input', (e) => {
      currentRadius = Number(e.target.value);
      radiusVal.textContent = currentRadius.toLocaleString() + ' m';
      renderLayers();
    });

    Papa.parse('https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv', {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: function(results) {
        accidentData = results.data
          .filter(d => typeof d.lng === 'number' && typeof d.lat === 'number')
          .map(d => [d.lng, d.lat]);

        const loader = document.getElementById('loader');
        if (loader) {
          loader.style.display = 'none';
        }

        renderLayers();
      },
      error: function(err) {
        const loaderText = document.getElementById('loader-text');
        if (loaderText) {
          loaderText.textContent = 'Failed to load dataset: ' + err;
        }
      }
    });
  </script>
</body>
</html>
```