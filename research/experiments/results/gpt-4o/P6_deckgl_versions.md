<!-- model: ac_7xhfwyml::openai::gpt-4o | prompt: P6_deckgl_versions | seconds: 5 | backend: litellm-proxy | usage: {"completion_tokens": 541, "prompt_tokens": 56, "total_tokens": 597, "completion_tokens_details": {"accepted_prediction_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0, "rejected_prediction_tokens": 0}, "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0}} -->
As of my last update in October 2023, the latest version of deck.gl is 8.11.0. Here’s a minimal example to render a `ScatterplotLayer` using deck.gl 8.11.0.

### Install Required Packages

Ensure you have Node.js installed, then create a new project directory and install the necessary packages using npm:

```bash
mkdir deckgl-scatterplot-example
cd deckgl-scatterplot-example
npm init -y
npm install @deck.gl/core@8.11.0 @deck.gl/react@8.11.0 react@18.2.0 react-dom@18.2.0
```

### Basic ScatterplotLayer Example

```jsx
// index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { DeckGL } from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

// Set your view state
const INITIAL_VIEW_STATE = {
  longitude: -122.45,
  latitude: 37.8,
  zoom: 12,
  pitch: 0,
  bearing: 0
};

// Define your data points
const data = [
  { position: [-122.45, 37.8] },
  { position: [-122.46, 37.81] }
];

const scatterplotLayer = new ScatterplotLayer({
  id: 'scatterplot-layer',
  data,
  getPosition: d => d.position,
  getRadius: 100,
  getFillColor: [255, 0, 0],
  pickable: true
});

function App() {
  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers={[scatterplotLayer]}
    />
  );
}

const rootElement = document.getElementById('root');
ReactDOM.render(<App />, rootElement);
```

### HTML File

Create a basic HTML file to hold your React app:

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>deck.gl ScatterplotLayer Example</title>
</head>
<body>
  <div id="root"></div>
  <script src="index.js" type="module"></script>
</body>
</html>
```

Run this setup using your favorite JavaScript bundler like webpack or Parcel. This minimal setup renders a scatterplot with red dots using deck.gl 8.11.0.