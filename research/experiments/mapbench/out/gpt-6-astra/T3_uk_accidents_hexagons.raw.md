```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Great Britain Road Accidents — 3D Hexagon Map</title>

  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css">
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.36/dist.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/d3-dsv@3.0.1/dist/d3-dsv.min.js"></script>

  <style>
    * { box-sizing: border-box; }
    html, body, #map {
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
    }
    body {
      background: #10151d;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #edf3fa;
    }
    #panel {
      position: absolute;
      top: 18px;
      left: 18px;
      z-index: 2;
      width: min(320px, calc(100vw - 80px));
      padding: 18px;
      border: 1px solid #ffffff25;
      border-radius: 12px;
      background: rgba(15, 21, 31, 0.94);
      box-shadow: 0 8px 30px #0006;
    }
    h1 { margin: 0 0 6px; font-size: 18px; }
    p { margin: 0; color: #aebccc; font-size: 12px; line-height: 1.5; }
    .slider-label {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 20px;
      font-size: 13px;
    }
    output { color: #72dedf; font-variant-numeric: tabular-nums; }
    input[type="range"] {
      width: 100%;
      margin: 12px 0 5px;
      accent-color: #58d3d6;
      cursor: pointer;
    }
    .ends {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #aebccc;
    }
    .legend {
      height: 9px;
      margin-top: 18px;
      margin-bottom: 6px;
      border-radius: 4px;
      background: linear-gradient(to right,
        #244c70, #287f95, #41b6b0, #a1dab4, #fed976, #f04b35);
    }
    #status { margin-top: 14px; }
    .hint { margin-top: 8px; font-size: 11px; }
    .error { color: #ffaaa0; }
    .deck-tooltip {
      border: 1px solid #ffffff30;
      border-radius: 7px;
      box-shadow: 0 4px 18px #0005;
    }
  </style>
</head>
<body>
  <div id="map" aria-label="3D hexagon map of road accident locations in Great Britain"></div>

  <section id="panel" aria-labelledby="title">
    <h1 id="title">Road accidents</h1>
    <p>Great Britain · 3D hexagonal aggregation</p>

    <div class="slider-label">
      <label for="radius">Hexagon radius</label>
      <output id="radius-value" for="radius">1,000 m</output>
    </div>
    <input id="radius" type="range" min="500" max="5000" step="100" value="1000">
    <div class="ends"><span>500 m</span><span>5,000 m</span></div>

    <div class="legend" aria-hidden="true"></div>
    <div class="ends"><span>Fewer accidents</span><span>More accidents</span></div>
    <p style="margin-top: 7px;">Color and height show the number of accidents per cell.</p>

    <p id="status" role="status" aria-live="polite">Loading accident locations…</p>
    <p class="hint">Hover for counts · Drag to pan · Scroll to zoom<br>Right-drag to rotate and tilt</p>
  </section>

  <script>
    "use strict";

    const DATA_URL =
      "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv";

    const INITIAL_VIEW_STATE = {
      longitude: -1.4157,
      latitude: 52.2324,
      zoom: 6.6,
      pitch: 45,
      bearing: -27
    };

    const map = new maplibregl.Map({
      container: "map",
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [INITIAL_VIEW_STATE.longitude, INITIAL_VIEW_STATE.latitude],
      zoom: INITIAL_VIEW_STATE.zoom,
      pitch: INITIAL_VIEW_STATE.pitch,
      bearing: INITIAL_VIEW_STATE.bearing,
      maxPitch: 75,
      antialias: true
    });

    map.addControl(new maplibregl.NavigationControl({
      visualizePitch: true
    }), "top-right");

    const lighting = new deck.LightingEffect({
      ambientLight: new deck.AmbientLight({
        color: [255, 255, 255],
        intensity: 1.0
      }),
      keyLight: new deck.DirectionalLight({
        color: [255, 243, 221],
        intensity: 1.7,
        direction: [-1, -3, -2]
      }),
      fillLight: new deck.DirectionalLight({
        color: [180, 213, 255],
        intensity: 0.6,
        direction: [2, 1, -1]
      })
    });

    const overlay = new deck.MapboxOverlay({
      interleaved: false,
      effects: [lighting],
      layers: [],
      getTooltip: ({object}) => {
        if (!object || !object.points) return null;
        const count = object.points.length;
        return {
          text: `${count.toLocaleString()} accident${count === 1 ? "" : "s"} in this cell`,
          style: {
            backgroundColor: "#101923",
            color: "#f1f6fc",
            fontFamily: "system-ui, sans-serif",
            fontSize: "13px",
            padding: "10px 13px"
          }
        };
      }
    });

    map.addControl(overlay);

    const slider = document.getElementById("radius");
    const radiusOutput = document.getElementById("radius-value");
    const status = document.getElementById("status");
    let points = null;

    function renderHexagons() {
      if (!points) return;

      overlay.setProps({
        layers: [
          new deck.HexagonLayer({
            id: "accident-hexagons",
            data: points,
            getPosition: d => d,
            radius: Number(slider.value),
            coverage: 0.9,
            extruded: true,
            pickable: true,
            autoHighlight: true,
            highlightColor: [255, 255, 255, 100],

            getColorWeight: 1,
            colorAggregation: "SUM",
            getElevationWeight: 1,
            elevationAggregation: "SUM",

            colorRange: [
              [36, 76, 112],
              [40, 127, 149],
              [65, 182, 176],
              [161, 218, 180],
              [254, 217, 118],
              [240, 75, 53]
            ],
            colorScaleType: "linear",
            elevationScaleType: "linear",
            elevationRange: [0, 18000],
            elevationScale: 1,
            lowerPercentile: 0,
            upperPercentile: 100,
            elevationLowerPercentile: 0,
            elevationUpperPercentile: 100,
            opacity: 0.92,
            material: {
              ambient: 0.35,
              diffuse: 0.65,
              shininess: 32,
              specularColor: [70, 80, 90]
            }
          })
        ]
      });
    }

    let pendingFrame = null;
    slider.addEventListener("input", () => {
      radiusOutput.value = `${Number(slider.value).toLocaleString()} m`;
      if (pendingFrame !== null) cancelAnimationFrame(pendingFrame);
      pendingFrame = requestAnimationFrame(() => {
        pendingFrame = null;
        renderHexagons();
      });
    });

    async function loadData() {
      try {
        const response = await fetch(DATA_URL);
        if (!response.ok) {
          throw new Error(`Dataset request failed (${response.status})`);
        }

        const csv = await response.text();
        points = d3.csvParse(csv.replace(/^\uFEFF/, ""), row => {
          if (!row.lng || !row.lat) return null;
          const lng = Number(row.lng);
          const lat = Number(row.lat);
          return Number.isFinite(lng) && Number.isFinite(lat) &&
                 Math.abs(lng) <= 180 && Math.abs(lat) <= 90
            ? [lng, lat]
            : null;
        });

        if (!points.length) throw new Error("No valid accident locations found");

        renderHexagons();
        status.textContent = `${points.length.toLocaleString()} accident locations loaded`;
      } catch (error) {
        console.error(error);
        status.classList.add("error");
        status.textContent = `Unable to load accident data: ${error.message}. Please reload to retry.`;
      }
    }

    loadData();
  </script>
</body>
</html>
```