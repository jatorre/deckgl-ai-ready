<!-- model: gpt-5.6-sol | prompt: P6_deckgl_versions | seconds: 24 | backend: codex-cli sandbox=read-only web_search=disabled -->
Target: deck.gl **9.1.14**.

Install:

```bash
npm install @deck.gl/core@9.1.14 @deck.gl/layers@9.1.14
```

HTML:

```html
<div id="map" style="width:100vw;height:100vh"></div>
```

JavaScript:

```js
import {Deck} from '@deck.gl/core';
import {ScatterplotLayer} from '@deck.gl/layers';

const data = [
  {position: [-122.4, 37.8], size: 100},
  {position: [-122.42, 37.76], size: 200}
];

new Deck({
  parent: document.getElementById('map'),
  initialViewState: {
    longitude: -122.4,
    latitude: 37.78,
    zoom: 11
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      id: 'points',
      data,
      getPosition: d => d.position,
      getRadius: d => d.size,
      getFillColor: [0, 128, 255, 180],
      radiusUnits: 'meters',
      pickable: true
    })
  ]
});
```

This uses deck.gl’s standalone `Deck` API and does not require React or a basemap library. Your bundler should give the `#map` element a full-height page; setting `body { margin: 0; }` is also useful.