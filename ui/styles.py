"""Self-contained styling so cloud routing cannot break decorative assets."""
from base64 import b64encode
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def stylesheet():
    root = Path(__file__).resolve().parents[1]
    css = (root / 'ui/theme.css').read_text()
    for asset, mime in (
        ('hermes-presence.png', 'image/png'),
        ('fonts/EBGaramond.ttf', 'font/ttf'),
    ):
        encoded = b64encode((root / 'static' / asset).read_bytes()).decode('ascii')
        css = css.replace(f'/app/static/{asset}', f'data:{mime};base64,{encoded}')
    return css
