<!-- model: ac_7xhfwyml::vertex::gemini-3.7-flash | prompt: P8_single_html_markers | seconds: 11 | backend: litellm-proxy | usage: {"completion_tokens": 1996, "prompt_tokens": 46, "total_tokens": 2042, "completion_tokens_details": {"reasoning_tokens": 1352, "text_tokens": 644}, "prompt_tokens_details": {"text_tokens": 46}} -->
Here is the complete, single-file HTML page using **Leaflet.js** and OpenStreetMap tiles.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>European Cities Interactive Map</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" 
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" 
        crossorigin="" />

  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body, html {
      height: 100%;
      width: 100%;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #map {
      height: 100%;
      width: 100%;
    }
    /* Floating Header Card */
    .header-card {
      position: absolute;
      top: 15px;
      left: 55px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(5px);
      padding: 10px 16px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
      font-size: 14px;
      color: #333;
    }
    .header-card h1 {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 2px;
    }
    /* Popup styling */
    .leaflet-popup-content-wrapper {
      border-radius: 8px;
      box-shadow: 0 3px 14px rgba(0, 0, 0, 0.2);
    }
    .leaflet-popup-content {
      margin: 12px 16px;
      font-size: 14px;
      line-height: 1.4;
    }
    .popup-title {
      font-size: 16px;
      font-weight: bold;
      color: #1a73e8;