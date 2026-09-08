```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Vancouver Property Values per m²</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- MapLibre GL JS -->
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css">
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>

  <!-- deck.gl standalone bundle -->
  <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>

  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #map {
      width: 100vw;
      height: 100vh;
      position: absolute;
      top: 0;
      left: 0;
    }
    #legend {
      position: absolute;
      bottom: 24px;
      right: 24px;
      background: rgba(255, 255, 255, 0.95);
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
      padding: 14px 18px;
      z-index: 10;
      min-width: 210px;
      pointer-events: auto;
    }
    #legend h3 {
      font-size: 13px;
      font-weight: 700;
      color: #1a1a1a;
      margin-bottom: 2px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    #legend .subtitle {
      font-size: 11px;
      color: #666;
      margin-bottom: 10px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      margin-bottom: 5px;
      font-size: 12px;
      color: #333;
    }
    .legend-item:last-child {
      margin-bottom: 0;
    }
    .color-swatch {
      width: 18px;
      height: 13px;
      margin-right: 9px;
      border-radius: 2px;
      border: 1px solid rgba(0, 0, 0, 0.12);
      flex-shrink: 0;
    }
    #loading {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(255, 255, 255, 0.92);
      padding: 12px 20px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      color: #333;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
      z-index: 20;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="loading">Loading Vancouver block data...</div>
  <div id="legend">
    <h3>Property Value</h3>
    <div class="subtitle">Value per m² (CAD)</div>
    <div id="legend-items"></div>
  </div>

  <script>
    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json';

    // 6-class sequential palette (YlOrRd adapted for choropleth on light basemap)
    const COLOR_RAMP = [
      [255, 255, 178, 205],
      [254, 204, 92, 210],
      [253, 141, 60, 215],
      [240, 59, 32, 220],
      [189, 0, 38, 225],
      [103, 0, 31, 235]
    ];

    let breaks = [];

    // Format currency numbers
    function formatVal(n) {
      if (n >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M';
      if (n >= 1000) return '$' + Math.round(n / 1000) + 'k';
      return '$' + Math.round(n);
    }

    function getColor(value) {
      if (value == null || isNaN(value)) return [180, 180, 180, 120];
      for (let i = 0; i < breaks.length; i++) {
        if (value <= breaks[i]) return COLOR_RAMP[i];
      }
      return COLOR_RAMP[COLOR_RAMP.length - 1];
    }

    // Initialize deck.gl with MapLibre basemap
    const deckOverlay = new deck.DeckGL({
      container: 'map',
      mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      initialViewState: {
        longitude: -123.10,
        latitude: 49.25,
        zoom: 11,
        pitch: 0,
        bearing: 0
      },
      controller: true,
      getTooltip: ({object}) => {
        if (!object || !object.properties) return null;
        const p = object.properties;
        const value = p.valuePerSqm != null
          ? '$' + Number(Math.round(p.valuePerSqm)).toLocaleString() + ' / m²'
          : 'N/A';
        const growth = p.growth != null
          ? (p.growth > 0 ? '+' : '') + Number(p.growth).toFixed(2) + '%'
          : 'N/A';

        return {
          html: `
            <div style="font-family: inherit; font-size: 12px; line-height: 1.5;">
              <div style="font-weight: 600; color: #111; margin-bottom: 3px; border-bottom: 1px solid #eee; padding-bottom: 3px;">Vancouver Block</div>
              <div><strong>Value:</strong> ${value}</div>
              <div><strong>Growth:</strong> ${growth}</div>
            </div>
          `,
          style: {
            backgroundColor: 'rgba(255, 255, 255, 0.96)',
            color: '#222',
            boxShadow: '0 3px 12px rgba(0, 0, 0, 0.15)',
            borderRadius: '5px',
            padding: '8px 11px',
            border: '1px solid rgba(0,0,0,0.06)'
          }
        };
      }
    });

    fetch(DATA_URL)
      .then(res => res.json())
      .then(geojson => {
        document.getElementById('loading').style.display = 'none';

        // Compute 6 quantile thresholds to handle extreme right skew
        const values = geojson.features
          .map(f => f.properties && f.properties.valuePerSqm)
          .filter(v => typeof v === 'number' && !isNaN(v) && v > 0)
          .sort((a, b) => a - b);

        const numClasses = COLOR_RAMP.length;
        breaks = [];
        for (let i = 1; i < numClasses; i++) {
          const idx = Math.floor((i / numClasses) * values.length);
          breaks.push(values[idx]);
        }

        // Build HTML legend
        const legendItems = document.getElementById('legend-items');
        const minVal = values[0];
        const maxVal = values[values.length - 1];

        for (let i = 0; i < numClasses; i++) {
          const lower = i === 0 ? minVal : breaks[i - 1];
          const upper = i === numClasses - 1 ? maxVal : breaks[i];
          const [r, g, b] = COLOR_RAMP[i];
          const label = i === numClasses - 1
            ? `${formatVal(lower)} +`
            : `${formatVal(lower)} – ${formatVal(upper)}`;

          const row = document.createElement('div');
          row.className = 'legend-item';
          row.innerHTML = `
            <span class="color-swatch" style="background: rgb(${r}, ${g}, ${b});"></span>
            <span>${label}</span>
          `;
          legendItems.appendChild(row);
        }

        // Add GeoJSON Layer
        const layer = new deck.GeoJsonLayer({
          id: 'vancouver-blocks',
          data: geojson,
          pickable: true,
          stroked: true,
          filled: true,
          extruded: false,
          lineWidthUnits: 'pixels',
          lineWidthMinPixels: 0.5,
          getLineColor: [255, 255, 255, 180],
          getLineWidth: 0.5,
          getFillColor: f => getColor(f.properties && f.properties.valuePerSqm),
          autoHighlight: true,
          highlightColor: [255, 255, 255, 120],
          updateTriggers: {
            getFillColor: [breaks]
          }
        });

        deckOverlay.setProps({ layers: [layer] });
      })
      .catch(err => {
        document.getElementById('loading').textContent = 'Error loading map data.';
        console.error(err);
      });
  </script>
</body>
</html>
```