<!-- model: ac_7xhfwyml::openai::gpt-5.2 | prompt: P1_large_points | seconds: 8 | backend: litellm-proxy | usage: {"completion_tokens": 583, "prompt_tokens": 73, "total_tokens": 656, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
**Recommendation (concrete stack):**  
- **Backend/tiling:** **tippecanoe** → **MBTiles** of your points (convert to **vector tiles**)  
- **Tile serving:** **tileserver-gl** (or **tegola**) to serve `/{z}/{x}/{y}.pbf`  
- **Frontend map:** **MapLibre GL JS** (WebGL, fast pan/zoom)  
- **Why:** 2M points as raw GeoJSON will stutter. Vector tiles + WebGL keep it smooth and only draw what’s on screen at the current zoom.

**Workflow (high level):**  
1) Build vector tiles:  
`tippecanoe -o points.mbtiles -zg --drop-densest-as-needed --extend-zooms-if-still-dropping points.geojson`  
2) Serve tiles with tileserver-gl (produces a TileJSON endpoint).  
3) Render in MapLibre with a circle layer styled by `speed`.

**Minimal HTML/JS example (MapLibre + speed color):**
```html
<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet"/>
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<div id="map" style="height:100vh"></div>
<script>
const map = new maplibregl.Map({
  container: "map",
  style: "https://demotiles.maplibre.org/style.json", // basemap
  center: [-122.42, 37.77],
  zoom: 10
});

map.on("load", () => {
  map.addSource("gps", {
    type: "vector",
    tiles: ["https://YOUR_TILESERVER/tiles/gps/{z}/{x}/{y}.pbf"],
    minzoom: 0, maxzoom: 14
  });

  map.addLayer({
    id: "gps-points",
    type: "circle",
    source: "gps",
    "source-layer": "points", // layer name inside the vector tiles
    paint: {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 6, 1, 12, 3],
      "circle-opacity": 0.8,
      "circle-color": ["interpolate", ["linear"], ["get","speed"],
        0, "#2c7bb6", 10, "#abd9e9", 20, "#ffffbf", 30, "#fdae61", 40, "#d7191c"]
    }
  });
});
</script>
```

This setup is the common “millions of points” pattern used in production.