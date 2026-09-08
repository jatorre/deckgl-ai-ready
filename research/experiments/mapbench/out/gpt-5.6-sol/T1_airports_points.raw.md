```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>World Airports</title>

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
    }

    body {
      font-family: Arial, Helvetica, sans-serif;
    }

    #legend {
      position: absolute;
      top: 12px;
      right: 12px;
      z-index: 10;
      min-width: 112px;
      padding: 10px 12px;
      color: #222;
      background: rgba(255, 255, 255, 0.94);
      border-radius: 5px;
      box-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
      pointer-events: none;
    }

    #legend-title {
      margin-bottom: 7px;
      font-size: 13px;
      font-weight: 700;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 5px 0;
      font-size: 12px;
    }

    .legend-dot {
      display: inline-block;
      flex: 0 0 auto;
      border: 1px solid rgba(0, 0, 0, 0.65);
      border-radius: 50%;
    }

    .major {
      width: 16px;
      height: 16px;
      background: rgb(230, 48, 62);
    }

    .mid {
      width: 12px;
      height: 12px;
      margin: 0 2px;
      background: rgb(255, 178, 0);
    }

    .small {
      width: 8px;
      height: 8px;
      margin: 0 4px;
      background: rgb(30, 136, 229);
    }

    #deck-tooltip {
      padding: 7px 9px !important;
      color: #fff !important;
      background: rgba(20, 20, 20, 0.92) !important;
      border-radius: 4px !important;
      font: 12px/1.4 Arial, Helvetica, sans-serif !important;
      white-space: pre-line;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <div id="legend" aria-label="Airport type legend">
    <div id="legend-title">Airport type</div>
    <div class="legend-item">
      <span class="legend-dot major"></span>
      <span>Major</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot mid"></span>
      <span>Mid</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot small"></span>
      <span>Small</span>
    </div>
  </div>

  <script>
    const DATA_URL =
      'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/airports.json';

    const TYPE_COLORS = {
      major: [230, 48, 62, 230],
      mid: [255, 178, 0, 230],
      small: [30, 136, 229, 230]
    };

    const TYPE_RADII = {
      major: 9,
      mid: 6,
      small: 4
    };

    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      center: [10, 20],
      zoom: 1.5,
      pitch: 0,
      bearing: 0,
      attributionControl: true
    });

    const overlay = new deck.MapboxOverlay({
      interleaved: false,
      layers: [],
      getTooltip: ({object}) => {
        if (!object) return null;
        return {
          text: `${object.name}\n${object.abbrev}`
        };
      },
      getCursor: ({isHovering}) => isHovering ? 'pointer' : 'grab'
    });

    map.addControl(overlay);

    fetch(DATA_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load airport data: ${response.status}`);
        }
        return response.json();
      })
      .then(airports => {
        overlay.setProps({
          layers: [
            new deck.ScatterplotLayer({
              id: 'airports',
              data: airports,
              pickable: true,
              opacity: 1,
              stroked: true,
              filled: true,
              radiusUnits: 'pixels',
              radiusMinPixels: 3,
              lineWidthUnits: 'pixels',
              lineWidthMinPixels: 1,
              getPosition: airport => airport.coordinates,
              getRadius: airport => TYPE_RADII[airport.type],
              getFillColor: airport => TYPE_COLORS[airport.type],
              getLineColor: [20, 20, 20, 210]
            })
          ]
        });
      })
      .catch(error => {
        console.error(error);
      });
  </script>
</body>
</html>
```