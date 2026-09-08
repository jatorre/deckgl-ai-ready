```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Great Britain Road Accidents — 3D Hexagons</title>

  <link
    rel="stylesheet"
    href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"
  >

  <script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@9.1.0/dist.min.js"></script>

  <style>
    html,
    body,
    #map {
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
      background: #090b10;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .control-panel {
      position: absolute;
      z-index: 10;
      top: 16px;
      left: 16px;
      width: min(310px, calc(100vw - 64px));
      padding: 14px 16px 16px;
      color: #f4f7fb;
      background: rgba(12, 16, 24, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 10px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(8px);
    }

    .control-panel h1 {
      margin: 0 0 5px;
      font-size: 16px;
      font-weight: 650;
      line-height: 1.25;
    }

    .control-panel p {
      margin: 0 0 14px;
      color: #aeb8c7;
      font-size: 12px;
      line-height: 1.4;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 7px;
      font-size: 13px;
    }

    #radius-value {
      color: #7dd3fc;
      font-variant-numeric: tabular-nums;
      font-weight: 650;
    }

    #radius {
      width: 100%;
      margin: 0;
      accent-color: #38bdf8;
      cursor: pointer;
    }

    .range-labels {
      display: flex;
      justify-content: space-between;
      margin-top: 4px;
      color: #7d8796;
      font-size: 10px;
    }

    #status {
      margin-top: 10px;
      color: #c9d2df;
      font-size: 11px;
    }

    .maplibregl-ctrl-attrib {
      background: rgba(10, 12, 17, 0.8) !important;
      color: #bbb;
    }

    .maplibregl-ctrl-attrib a {
      color: #8bcdf2;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <section class="control-panel" aria-label="Hexagon map controls">
    <h1>Great Britain Road Accidents</h1>
    <p>Hexagon color and height represent the number of accident locations.</p>

    <div class="slider-header">
      <label for="radius">Hexagon radius</label>
      <span id="radius-value">1,000 m</span>
    </div>

    <input
      id="radius"
      type="range"
      min="500"
      max="5000"
      step="100"
      value="1000"
    >

    <div class="range-labels">
      <span>500 m</span>
      <span>5,000 m</span>
    </div>

    <div id="status">Loading accident data…</div>
  </section>

  <script>
    const DATA_URL =
      "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv";

    const INITIAL_VIEW = {
      longitude: -1.4157,
      latitude: 52.2324,
      zoom: 6.6,
      pitch: 45,
      bearing: -27
    };

    const map = new maplibregl.Map({
      container: "map",
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [INITIAL_VIEW.longitude, INITIAL_VIEW.latitude],
      zoom: INITIAL_VIEW.zoom,
      pitch: INITIAL_VIEW.pitch,
      bearing: INITIAL_VIEW.bearing,
      attributionControl: true,
      antialias: true
    });

    const ambientLight = new deck.AmbientLight({
      color: [255, 255, 255],
      intensity: 1.0
    });

    const directionalLight = new deck.DirectionalLight({
      color: [255, 245, 230],
      intensity: 1.8,
      direction: [-3, -7, -2]
    });

    const lightingEffect = new deck.LightingEffect({
      ambientLight,
      directionalLight
    });

    const overlay = new deck.MapboxOverlay({
      interleaved: false,
      layers: [],
      effects: [lightingEffect],
      getTooltip: ({object}) => {
        if (!object) return null;

        const count =
          object.points?.length ??
          object.count ??
          object.elevationValue ??
          object.colorValue ??
          0;

        return {
          text: `${Math.round(count).toLocaleString()} accident location${Math.round(count) === 1 ? "" : "s"}`,
          style: {
            backgroundColor: "rgba(10, 14, 22, 0.94)",
            color: "#ffffff",
            fontSize: "13px",
            padding: "8px 10px",
            borderRadius: "6px",
            border: "1px solid rgba(255,255,255,0.18)"
          }
        };
      }
    });

    map.on("load", () => {
      map.addControl(overlay);
    });

    const radiusInput = document.getElementById("radius");
    const radiusValue = document.getElementById("radius-value");
    const status = document.getElementById("status");

    let accidentPoints = [];

    function createHexagonLayer(radius) {
      return new deck.HexagonLayer({
        id: "accident-hexagons",
        data: accidentPoints,
        getPosition: point => point,
        radius,
        extruded: true,
        pickable: true,
        coverage: 0.88,
        elevationScale: 20,
        getColorValue: points => points.length,
        getElevationValue: points => points.length,
        gpuAggregation: false,
        colorRange: [
          [32, 75, 122],
          [38, 145, 165],
          [61, 190, 137],
          [178, 216, 75],
          [249, 173, 52],
          [220, 55, 47]
        ],
        colorScaleType: "quantize",
        material: {
          ambient: 0.35,
          diffuse: 0.65,
          shininess: 32,
          specularColor: [90, 90, 90]
        },
        transitions: {
          elevationScale: 300
        }
      });
    }

    function renderLayer() {
      const radius = Number(radiusInput.value);
      radiusValue.textContent = `${radius.toLocaleString()} m`;

      overlay.setProps({
        layers: [createHexagonLayer(radius)],
        effects: [lightingEffect]
      });
    }

    radiusInput.addEventListener("input", renderLayer);

    fetch(DATA_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.text();
      })
      .then(csv => {
        const lines = csv.trim().split(/\r?\n/);
        accidentPoints = [];

        for (let i = 1; i < lines.length; i++) {
          const comma = lines[i].indexOf(",");
          if (comma === -1) continue;

          const longitude = Number(lines[i].slice(0, comma));
          const latitude = Number(lines[i].slice(comma + 1));

          if (Number.isFinite(longitude) && Number.isFinite(latitude)) {
            accidentPoints.push([longitude, latitude]);
          }
        }

        status.textContent =
          `${accidentPoints.length.toLocaleString()} locations loaded`;
        renderLayer();
      })
      .catch(error => {
        console.error(error);
        status.textContent = "Unable to load the accident dataset.";
        status.style.color = "#fca5a5";
      });
  </script>
</body>
</html>
```