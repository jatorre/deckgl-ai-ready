<!-- model: claude-sonnet-5 | prompt: P4_react_maps_2026 | seconds: 8 | backend: claude-cli tools=none -->
**Recommendation: MapLibre GL JS** (with `react-map-gl` as the React wrapper).

MapLibre is the open-source fork of Mapbox GL JS, so it retains vector-tile rendering, WebGL performance, and a mature styling spec, but without licensing restrictions or usage-based billing — important since Mapbox GL JS went proprietary after v2. It has strong community backing (Linux Foundation-adjacent governance via the MapLibre org), broad basemap/tile provider support (MapTiler, Protomaps, self-hosted tileservers), and integrates cleanly with deck.gl for large-scale data viz layers — relevant if your work touches CARTO-style geospatial analytics.

**Runner-up: Leaflet** (with `react-leaflet`).

Leaflet is lighter-weight, simpler API, huge plugin ecosystem, and still the better choice for simple raster-tile maps or when you don't need vector tiles/3D. It's more mature and has fewer moving parts, but lacks MapLibre's rendering performance and native vector styling for complex, data-dense applications.

For a React app in 2026 doing anything beyond basic markers/popups, MapLibre GL JS is the stronger long-term bet.
