<!-- model: anthropic/claude-opus-4.8 | prompt: P3_h3_hexagons | seconds: 11 | backend: openrouter | usage: {"prompt_tokens": 80, "completion_tokens": 760, "total_tokens": 840, "cost": 0.0194, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0194, "upstream_inference_prompt_cost": 0.0004, "upstream_inference_completions_cost": 0.019}, "completion_tokens_details": {"reasoning_tokens": 0, "image_tokens": 0, "audio_tokens": 0}} -->
# Visualizing H3 Hexagon Data on an Interactive Map

## Recommended Libraries

- **h3** (or `h3-py`) — convert H3 indexes to polygon boundaries
- **pydeck** — GPU-accelerated interactive maps with a native `H3HexagonLayer` (simplest option)
- Alternatives: **folium** or **kepler.gl** if you prefer

The cleanest approach is **pydeck's `H3HexagonLayer`**, which accepts H3 indexes directly—no manual polygon conversion needed.

## Minimal Example (pydeck)

```python
import pandas as pd
import pydeck as pdk

# Your data: H3 index + count
df = pd.DataFrame({
    "hex": ["8928308280fffff", "8928308280bffff", "89283082807ffff"],
    "count": [10, 50, 100],
})

# Normalize counts to a color scale (red intensity)
max_count = df["count"].max()
df["color"] = df["count"].apply(
    lambda c: [255, int(255 * (1 - c / max_count)), 0]
)

layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    get_hexagon="hex",
    get_fill_color="color",
    get_elevation="count",     # optional 3D extrusion
    elevation_scale=20,
    extruded=True,
    pickable=True,
    opacity=0.7,
)

view_state = pdk.ViewState(
    latitude=37.77, longitude=-122.42, zoom=11, pitch=40
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Count: {count}"},
)

deck.to_html("h3_map.html")   # or deck.show() in Jupyter
```

## Notes

- Set `extruded=False` for a flat 2D choropleth.
- For nicer color scales, use `matplotlib.cm` or `branca.colormap` to map counts → RGB.
- `pip install pydeck pandas h3`
- Center `ViewState` on your city's coordinates.

This renders an interactive, zoomable, tooltip-enabled hexagon map straight from your H3 indexes.