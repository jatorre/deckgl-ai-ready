```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vancouver Property Values</title>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css">
  <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/deck.gl@8.9.36/dist.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    html, body, #map { width: 100%; height: 100%; margin: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; color: #243447; }
    #map { position: absolute; inset: 0; }
    #legend {
      position: absolute;
      z-index: 10;
      left: 16px;
      bottom: 32px;
      width: 280px;
      max-width: calc(100vw - 32px);
      padding: 16px;
      background: rgba(255, 255, 255, 0.96);
      border: 1px solid #dce3e9;
      border-radius: 8px;
      box-shadow: 0 3px 18px #00000018;
      pointer-events: auto;
    }
    h1 { margin: 0 0 4px; font-size: 17px; }
    .subtitle { margin: 0 0 13px; color: #526372; font-size: 12px; }
    .legend-row { display: flex; align-items: center; gap: 10px; margin: 7px 0; font-size: 12px; }
    .swatch {
      flex: 0 0 25px;
      height: 15px;
      border: 1px solid #00000018;
      border-radius: 2px;
    }
    .note { margin: 12px 0 0; font-size: 11px; line-height: 1.5; color: #526372; }
    #status { font-size: 12px; line-height: 1.5; }
    .error { color: #a12626; }
    a { color: #245b86; }
  </style>
</head>
<body>
  <div id="map" aria-label="Interactive choropleth map of Vancouver property values"></div>
  <aside id="legend" aria-label="Map legend">
    <h1>Vancouver property values</h1>
    <p class="subtitle">Value per square metre · 6 quantile classes</p>
    <div id="status" role="status" aria-live="polite">Loading polygon data…</div>
    <div id="classes"></div>
    <p class="note">
      Quantiles place approximately equal numbers of blocks in each class,
      revealing variation despite the strongly skewed values. Hover over a block for details.
    </p>
    <p class="note">
      Data:
      <a href="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
         target="_blank" rel="noopener noreferrer">deck.gl Vancouver blocks</a>
    </p>
  </aside>

  <script>
    const DATA_URL =
      'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json';

    // ColorBrewer's six-class sequential Blues palette.
    const COLORS = [
      [239, 243, 255],
      [198, 219, 239],
      [158, 202, 225],
      [107, 174, 214],
      [49, 130, 189],
      [8, 81, 156]
    ];
    const NO_DATA_COLOR = [195, 195, 195];
    const numberFormat = new Intl.NumberFormat('en-CA', {
      maximumFractionDigits: 6
    });
    const formatNumber = value =>
      typeof value === 'number' && Number.isFinite(value)
        ? numberFormat.format(value)
        : 'No data';

    const map = new deck.DeckGL({
      container: 'map',
      map: maplibregl,
      mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      initialViewState: {
        longitude: -123.10,
        latitude: 49.25,
        zoom: 11,
        pitch: 0,
        bearing: 0
      },
      controller: true,
      layers: [],
      getTooltip: ({object}) => object ? {
        text:
          `Value per m² (valuePerSqm): ${formatNumber(object.properties.valuePerSqm)}\n` +
          `Growth: ${formatNumber(object.properties.growth)}`,
        style: {
          backgroundColor: '#ffffff',
          color: '#243447',
          fontSize: '13px',
          padding: '10px 12px',
          border: '1px solid #dce3e9',
          borderRadius: '5px',
          boxShadow: '0 2px 12px #00000025'
        }
      } : null
    });

    function addLegendRow(color, label) {
      const row = document.createElement('div');
      row.className = 'legend-row';
      const swatch = document.createElement('span');
      swatch.className = 'swatch';
      swatch.style.backgroundColor = `rgb(${color.join(',')})`;
      const text = document.createElement('span');
      text.textContent = label;
      row.append(swatch, text);
      document.getElementById('classes').appendChild(row);
    }

    async function loadData() {
      const status = document.getElementById('status');
      try {
        const response = await fetch(DATA_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const geojson = await response.json();
        if (geojson.type !== 'FeatureCollection' || !Array.isArray(geojson.features)) {
          throw new Error('The response is not a GeoJSON FeatureCollection.');
        }

        const validValue = value =>
          typeof value === 'number' && Number.isFinite(value);

        const values = geojson.features
          .map(feature => feature.properties.valuePerSqm)
          .filter(validValue)
          .sort((a, b) => a - b);

        if (!values.length) throw new Error('No numeric valuePerSqm values found.');

        // Nearest-rank quantiles, computed from the real dataset.
        // Equal values stay together; thresholds belong to the lower class.
        const thresholds = Array.from({length: 5}, (_, i) =>
          values[Math.ceil(values.length * (i + 1) / 6) - 1]
        );
        const bounds = [values[0], ...thresholds, values[values.length - 1]];

        function fillColor(feature) {
          const value = feature.properties.valuePerSqm;
          if (!validValue(value)) return NO_DATA_COLOR;
          let index = 0;
          while (index < thresholds.length && value > thresholds[index]) index++;
          return COLORS[index];
        }

        map.setProps({
          layers: [
            new deck.GeoJsonLayer({
              id: 'vancouver-value-choropleth',
              data: geojson,
              filled: true,
              stroked: true,
              extruded: false,
              pickable: true,
              getFillColor: fillColor,
              getLineColor: [250, 250, 250, 220],
              getLineWidth: 0.5,
              lineWidthUnits: 'pixels',
              lineWidthMinPixels: 0.5,
              autoHighlight: true,
              highlightColor: [255, 190, 70, 110]
            })
          ]
        });

        COLORS.forEach((color, i) => {
          const lower = formatNumber(bounds[i]);
          const upper = formatNumber(bounds[i + 1]);
          addLegendRow(
            color,
            i === 0 ? `${lower} ≤ value ≤ ${upper}` : `${lower} < value ≤ ${upper}`
          );
        });

        const missingCount = geojson.features.length - values.length;
        if (missingCount) addLegendRow(NO_DATA_COLOR, 'No data');

        status.textContent = `${geojson.features.length.toLocaleString('en-CA')} blocks loaded`;
        status.style.marginBottom = '10px';
      } catch (error) {
        console.error(error);
        status.className = 'error';
        status.textContent = `Could not load the dataset: ${error.message}`;
      }
    }

    loadData();
  </script>
</body>
</html>
```