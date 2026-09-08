```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Vancouver Blocks Property Value Map</title>
  <style>
    body, html {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #map-container {
      width: 100%;
      height: 100%;
      position: absolute;
    }
    #legend {
      position: absolute;
      bottom: 40px;
      right: 20px;
      background: white;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 1000;
      pointer-events: none;
    }
    #legend h3 {
      margin: 0 0 12px 0;
      font-size: 14px;
      color: #333;
    }
    .legend-item {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
      font-size: 12px;
      color: #555;
    }
    .legend-item:last-child {
      margin-bottom: 0;
    }
    .color-box {
      width: 16px;
      height: 16px;
      margin-right: 12px;
      border: 1px solid rgba(0,0,0,0.1);
      border-radius: 2px;
    }
  </style>
  
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
  
  <!-- Alias maplibregl to mapboxgl so deck.gl can use it automatically -->
  <script>window.mapboxgl = maplibregl;</script>
  
  <script src="https://unpkg.com/deck.gl@8.9.32/dist.min.js"></script>
</head>
<body>

  <div id="map-container"></div>
  <div id="legend"></div>

  <script>
    const DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json';
    const BASEMAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';
    
    // Sequential color scheme (Yellow-Orange-Red) for 6 classes
    const COLORS = [
      [255, 255, 178],
      [254, 217, 118],
      [254, 178, 76],
      [253, 141, 60],
      [240, 59, 32],
      [189, 0, 38]
    ];

    const deckgl = new deck.DeckGL({
      container: 'map-container',
      mapStyle: BASEMAP_STYLE,
      initialViewState: {
        longitude: -123.10,
        latitude: 49.25,
        zoom: 11,
        pitch: 0,
        bearing: 0
      },
      controller: true,
      getTooltip: ({object}) => {
        if (!object) return null;
        const val = object.properties.valuePerSqm;
        const growth = object.properties.growth;
        return {
          html: `
            <div style="font-family: sans-serif; font-size: 13px;">
              <b>Value per Sqm:</b> ${val !== undefined && val !== null ? val.toLocaleString(undefined, {maximumFractionDigits: 2}) : 'N/A'}<br/>
              <b>Growth:</b> ${growth !== undefined && growth !== null ? growth.toLocaleString(undefined, {maximumFractionDigits: 2}) : 'N/A'}
            </div>
          `,
          style: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '10px',
            borderRadius: '4px'
          }
        };
      },
      layers: []
    });

    fetch(DATA_URL)
      .then(response => response.json())
      .then(data => {
        // Extract and sort non-null values to calculate quantile breaks
        const values = data.features
          .map(f => f.properties.valuePerSqm)
          .filter(v => v !== null && v !== undefined)
          .sort((a, b) => a - b);
          
        const numClasses = COLORS.length;
        const breaks = [];
        
        for (let i = 1; i < numClasses; i++) {
          breaks.push(values[Math.floor((values.length - 1) * (i / numClasses))]);
        }

        // Build HTML Legend
        const legendDiv = document.getElementById('legend');
        let legendHTML = '<h3>Value per Sqm (Quantiles)</h3>';
        for (let i = 0; i < numClasses; i++) {
          const color = COLORS[i];
          const min = i === 0 ? Math.min(...values) : breaks[i - 1];
          const max = i === numClasses - 1 ? Math.max(...values) : breaks[i];
          
          const minStr = Math.round(min).toLocaleString();
          const maxStr = Math.round(max).toLocaleString();
          
          legendHTML += `
            <div class="legend-item">
              <div class="color-box" style="background: rgb(${color.join(',')})"></div>
              <span>${minStr} &ndash; ${maxStr}</span>
            </div>
          `;
        }
        legendDiv.innerHTML = legendHTML;

        function getFillColor(val) {
          if (val === null || val === undefined) return [200, 200, 200, 150];
          for (let i = 0; i < breaks.length; i++) {
            if (val <= breaks[i]) return COLORS[i];
          }
          return COLORS[COLORS.length - 1];
        }

        const geoJsonLayer = new deck.GeoJsonLayer({
          id: 'vancouver-blocks-layer',
          data: data,
          pickable: true,
          stroked: true,
          filled: true,
          lineWidthMinPixels: 1,
          getLineColor: [255, 255, 255, 180],
          getFillColor: d => getFillColor(d.properties.valuePerSqm)
        });

        deckgl.setProps({
          layers: [geoJsonLayer]
        });
      })
      .catch(error => console.error('Error loading GeoJSON:', error));
  </script>
</body>
</html>
```