```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Airports Map</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  <style>
    html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
    #map { position: absolute; width: 100%; height: 100%; }
    #legend {
      position: absolute;
      bottom: 20px;
      left: 20px;
      background: rgba(255,255,255,0.9);
      padding: 10px 14px;
      border-radius: 6px;
      font-family: sans-serif;
      font-size: 13px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.3);
      z-index: 1;
    }
    #legend h4 { margin: 0 0 6px 0; font-size: 14px; }
    .legend-row { display: flex; align-items: center; margin: 3px 0; }
    .legend-dot { width: 14px; height: 14px; border-radius: 50%; margin-right: 8px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="legend">
    <h4>Airport Type</h4>
    <div class="legend-row"><span class="legend-dot" style="background:rgb(230,50,50)"></span>Major</div>
    <div class="legend-row"><span class="legend-dot" style="background:rgb(50,140,230)"></span>Mid</div>
    <div class="legend-row"><span class="legend-dot" style="background:rgb(70,190,90)"></span>Small</div>
  </div>
  <script>
    const {DeckGL, ScatterplotLayer} = deck;

    const COLORS = {
      major: [230, 50, 50],
      mid:   [50, 140, 230],
      small: [70, 190, 90]
    };
    const RADII = {
      major: 30000,
      mid:   18000,
      small: 10000
    };

    new DeckGL({
      container: 'map',
      mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      initialViewState: {
        longitude: 10,
        latitude: 20,
        zoom: 1.5,
        pitch: 0,
        bearing: 0
      },
      controller: true,
      layers: [
        new ScatterplotLayer({
          id: 'airports',
          data: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/airports.json',
          getPosition: d => d.coordinates,
          getFillColor: d => COLORS[d.type] || [150, 150, 150],
          getRadius: d => RADII[d.type] || 8000,
          radiusUnits: 'meters',
          radiusMinPixels: 3,
          radiusMaxPixels: 30,
          stroked: true,
          getLineColor: [255, 255, 255],
          lineWidthMinPixels: 0.5,
          pickable: true
        })
      ],
      getTooltip: ({object}) =>
        object && {
          html: `<b>${object.name}</b><br/>${object.abbrev || ''}`,
          style: {
            backgroundColor: 'rgba(0,0,0,0.8)',
            color: '#fff',
            fontFamily: 'sans-serif',
            fontSize: '12px',
            padding: '6px 8px',
            borderRadius: '4px'
          }
        }
    });
  </script>
</body>
</html>
```