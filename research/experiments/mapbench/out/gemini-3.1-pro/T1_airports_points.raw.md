```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Airports Map</title>
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  <script src="https://unpkg.com/deck.gl@8.9.33/dist.min.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      font-family: Arial, sans-serif;
    }
    #map-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
    }
    #legend {
      position: absolute;
      bottom: 30px;
      right: 30px;
      background: white;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      z-index: 10;
      font-size: 14px;
      color: #333;
    }
    .legend-title {
      font-weight: bold;
      margin-bottom: 12px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      margin-bottom: 8px;
    }
    .legend-item:last-child {
      margin-bottom: 0;
    }
    .legend-color-container {
      width: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-right: 10px;
    }
    .legend-color {
      border-radius: 50%;
      border: 1px solid #fff;
      box-shadow: 0 0 2px rgba(0,0,0,0.3);
    }
  </style>
</head>
<body>
  <div id="map-container"></div>
  
  <div id="legend">
    <div class="legend-title">Airport Type</div>
    <div class="legend-item">
      <div class="legend-color-container">
        <div class="legend-color" style="background: rgb(228, 26, 28); width: 16px; height: 16px;"></div>
      </div>
      Major
    </div>
    <div class="legend-item">
      <div class="legend-color-container">
        <div class="legend-color" style="background: rgb(55, 126, 184); width: 10px; height: 10px;"></div>
      </div>
      Mid
    </div>
    <div class="legend-item">
      <div class="legend-color-container">
        <div class="legend-color" style="background: rgb(77, 175, 74); width: 6px; height: 6px;"></div>
      </div>
      Small
    </div>
  </div>

  <script>
    window.mapboxgl = maplibregl;

    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/airports.json';

    const INITIAL_VIEW_STATE = {
      longitude: 10,
      latitude: 20,
      zoom: 1.5,
      pitch: 0,
      bearing: 0
    };

    const airportsLayer = new deck.ScatterplotLayer({
      id: 'airports-layer',
      data: DATA_URL,
      pickable: true,
      opacity: 0.9,
      stroked: true,
      filled: true,
      radiusUnits: 'pixels',
      lineWidthUnits: 'pixels',
      getLineWidth: 1,
      getLineColor: [255, 255, 255],
      getPosition: d => d.coordinates,
      getRadius: d => {
        if (d.type === 'major') return 8;
        if (d.type === 'mid') return 5;
        return 3;
      },
      getFillColor: d => {
        if (d.type === 'major') return [228, 26, 28];
        if (d.type === 'mid') return [55, 126, 184];
        return [77, 175, 74];
      }
    });

    new deck.DeckGL({
      container: 'map-container',
      mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      initialViewState: INITIAL_VIEW_STATE,
      controller: true,
      getTooltip: ({object}) => object && `${object.name} (${object.abbrev})`,
      layers: [airportsLayer]
    });
  </script>
</body>
</html>
```