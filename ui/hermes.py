"""A genuine low-resolution 3D voxel portrait, rendered locally in the browser."""

from pathlib import Path

from streamlit.components.v2 import component

_PORTRAIT = component(
    "hermes_voxel",
    html='''<div class="portrait">
      <canvas width="168" height="144" tabindex="0" role="img"
        aria-label="Interactive 3D voxel portrait of Hermes Trismegistus. Drag to rotate, use arrow keys to turn, or Home to reset."></canvas>
      <img class="fallback" src="/app/static/hermes-pixel.png"
        alt="Pixel-art portrait of Hermes Trismegistus" hidden>
    </div>''',
    css='''
      :host { display: block; }
      .portrait { height: 240px; display: grid; place-items: center; }
      canvas { width: 280px; height: 240px; max-width: 100%;
        image-rendering: pixelated; cursor: grab; touch-action: pan-y;
        outline: none; -webkit-tap-highlight-color: transparent; }
      canvas:active { cursor: grabbing; }
      canvas:focus-visible { outline: 1px solid #a94a61; outline-offset: -10px; }
      .fallback { width: 240px; height: 240px; object-fit: cover;
        object-position: right; image-rendering: pixelated; }
      [hidden] { display: none !important; }
    ''',
    js=Path(__file__).with_name("hermes.js").read_text(),
)


def render_hermes():
    """Mount trusted static code; no visitor input is passed into JavaScript."""
    _PORTRAIT(key="hermes_portrait", height=240)
