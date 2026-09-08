<!-- model: openai/gpt-6-astra | prompt: P3_h3_hexagons | seconds: 20 | backend: openrouter | usage: {"prompt_tokens": 59, "completion_tokens": 730, "total_tokens": 789, "cost": 0.03709, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.03709, "upstream_inference_prompt_cost": 0.00059, "upstream_inference_completions_cost": 0.0365}, "completion_tokens_details": {"reasoning_tokens": 205, "image_tokens": 0, "audio_tokens": 0}} -->
**Recommended libraries**
- **deck.gl + MapLibre GL JS** for a JavaScript application. deck.gl’s `H3HexagonLayer` renders existing H3 cells directly; MapLibre supplies the interactive basemap.
- **pydeck** (a Python wrapper for deck.gl) for the quickest route from a table to an interactive HTML map.
- **h3-py** only if you need to create or manipulate H3 indexes; existing indexes need no conversion.

### Minimal Python example

```bash
pip install pydeck pandas "h3>=4"
```

```python
import h3
import pandas as pd
import pydeck as pdk

# Example data over San Francisco.
# Replace with: df = pd.read_csv("counts.csv")
# Required columns: h3_index (hexadecimal string), count (numeric).
df = pd.DataFrame([
    {"h3_index": h3.latlng_to_cell(lat, lon, 8), "count": count}
    for lat, lon, count in [
        (37.775, -122.418, 10),
        (37.795, -122.408, 50),
        (37.755, -122.438, 100),
    ]
])

# Light-to-dark blue, normalized to the observed count range.
lo, hi = df["count"].min(), df["count"].max()
df["color"] = [
    [int(230 - 200*t), int(240 - 140*t), 220, 210]
    for t in (df["count"] - lo) / max(hi - lo, 1)
]

layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    get_hexagon="h3_index",
    get_fill_color="color",
    pickable=True,
    extruded=False,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=pdk.ViewState(
        latitude=37.775, longitude=-122.418, zoom=11
    ),
    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
    tooltip={"text": "H3: {h3_index}\nCount: {count}"},
)
deck.to_html("city_hexagons.html", open_browser=True)
```

The output supports pan, zoom, and hover. Basemap tiles and visualization scripts require internet access. For production, add a count legend and consider logarithmic coloring for skewed counts.