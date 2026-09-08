<!-- model: gpt-5.6-sol | prompt: P1_large_points | seconds: 39 | backend: codex-cli sandbox=read-only web_search=disabled -->
Use **MapLibre GL JS + deck.gl**. MapLibre renders the basemap; deck.gl’s GPU-backed `ScatterplotLayer` renders millions of points efficiently. Serve data as spatially partitioned binary tiles—Apache Arrow or packed typed arrays—not GeoJSON. Load only visible tiles and use level-of-detail aggregation at low zooms.

```html
<div id="map" style="position:fixed;inset:0"></div>
<script type="module">
import maplibregl from "https://esm.sh/maplibre-gl@5";
import {MapboxOverlay} from "https://esm.sh/@deck.gl/mapbox@9";
import {ScatterplotLayer} from "https://esm.sh/@deck.gl/layers@9";
import "https://esm.sh/maplibre-gl@5/dist/maplibre-gl.css";

const map = new maplibregl.Map({
  container: "map",
  style: "https://demotiles.maplibre.org/style.json",
  center: [-3.7, 40.4],
  zoom: 5
});

// Your API should return packed Float32 triples: longitude, latitude, speed.
const packed = new Float32Array(
  await (await fetch("/points.bin")).arrayBuffer()
);

const count = packed.length / 3;
const positions = new Float32Array(count * 2);
const colors = new Uint8Array(count * 4);

for (let i = 0; i < count; i++) {
  positions.set([packed[i*3], packed[i*3+1]], i*2);
  const t = Math.min(packed[i*3+2] / 120, 1);
  colors.set([255*t, 180*(1-t), 255*(1-t), 190], i*4);
}

map.addControl(new MapboxOverlay({
  layers: [new ScatterplotLayer({
    id: "gps",
    data: {
      length: count,
      attributes: {
        getPosition: {value: positions, size: 2},
        getFillColor: {value: colors, size: 4}
      }
    },
    radiusMinPixels: 1,
    radiusMaxPixels: 5
  })]
}));
</script>
```

For production, use a tile endpoint and Web Workers to decode Arrow/binary data off the main thread. Avoid Leaflet and raw GeoJSON for this volume.