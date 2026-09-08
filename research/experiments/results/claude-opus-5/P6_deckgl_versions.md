<!-- model: claude-opus-5 | prompt: P6_deckgl_versions | seconds: 18 | backend: claude-cli tools=none -->
## Version

Targeting **deck.gl 9.1.x** — the latest line I'm aware of as of my May 2026 knowledge cutoff. A newer minor may exist; confirm with `npm view deck.gl version` before pinning.

## Install

```bash
npm install @deck.gl/core@^9.1.0 @deck.gl/layers@^9.1.0
```

Keep both scoped packages on the same version — mismatched deck.gl submodules break at runtime. `luma.gl` and `@math.gl/*` come in transitively; don't install them yourself. (The umbrella `deck.gl@^9.1.0` package works too and bundles every layer module, at a larger bundle cost.)

## Example

```js
import {Deck} from '@deck.gl/core';
import {ScatterplotLayer} from '@deck.gl/layers';

const data = [
  {position: [-122.42, 37.78], size: 500, name: 'San Francisco'},
  {position: [-74.01, 40.71], size: 800, name: 'New York'},
  {position: [-0.13, 51.51], size: 700, name: 'London'}
];

new Deck({
  initialViewState: {
    longitude: -50,
    latitude: 45,
    zoom: 2
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      id: 'cities',
      data,
      getPosition: d => d.position,
      getRadius: d => d.size,
      getFillColor: [255, 140, 0],
      radiusUnits: 'meters',
      radiusMinPixels: 3,
      pickable: true
    })
  ],
  getTooltip: ({object}) => object && object.name
});
```

## Notes

- With no `parent` or `canvas` option, `Deck` creates a full-window canvas appended to `document.body`. Pass `parent: document.getElementById('map')` to scope it to a container — the container needs an explicit height and `position: relative`.
- `radiusMinPixels` is what keeps points visible when zoomed out; without it they shrink to nothing.
- There's no basemap here. Adding one means a separate library (`react-map-gl`/MapLibre) and its own peer deps.
