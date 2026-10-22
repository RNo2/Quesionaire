"""A decorative, viewport-scale presence with restrained pointer parallax."""

from pathlib import Path

from streamlit.components.v2 import component

_PRESENCE = component(
    "hermes_presence",
    html="<span hidden></span>",
    js=Path(__file__).with_name("presence.js").read_text(),
)


def render_presence():
    _PRESENCE(key="hermes_presence", height=0)
