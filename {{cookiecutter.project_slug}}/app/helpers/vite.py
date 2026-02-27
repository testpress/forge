import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

from django import template
from django.conf import settings

register = template.Library()

VITE_DEV_SERVER: str = getattr(settings, "VITE_DEV_SERVER_URL", "http://localhost:5173")


def is_vite_dev() -> bool:
    return settings.DEBUG and os.environ.get("VITE_DEV_SERVER", "1") != "0"


@lru_cache
def load_manifest() -> dict[str, dict[str, str]]:
    base_dir = getattr(settings, "BASE_DIR", Path(__file__).resolve().parent.parent)
    manifest_path = base_dir / getattr(
        settings, "VITE_MANIFEST_PATH", "app/static/dist/.vite/manifest.json"
    )

    if not manifest_path.exists():
        msg = "Vite manifest.json not found. Run `npm run build` first."
        raise FileNotFoundError(msg)

    with manifest_path.open() as f:
        data: Any = json.load(f)
        return cast(dict[str, dict[str, str]], data)


@register.simple_tag
def vite_static(path: str) -> str:
    """
    Load Vite assets dynamically based on environment.
    
    Development: Returns http://localhost:5173/{path}
    Production: Returns {STATIC_URL}{hashed_file} from manifest.json
    
    Usage:
        {% raw %}{% load vite %}
        <link rel="stylesheet" href="{% vite_static 'css/styles.css' %}" />
        <script type="module" src="{% vite_static 'js/main.js' %}"></script>{% endraw %}
    
    Note: Path must match exactly as it appears in Vite's manifest.json
    """
    # Development: use Vite dev server
    if is_vite_dev():
        return f"{VITE_DEV_SERVER}/{path}"

    # Production: read from manifest
    manifest: dict[str, dict[str, str]] = load_manifest()

    # Get hashed filename from manifest
    hashed: dict[str, str] | None = manifest.get(path)
    if hashed is None:
        msg = (
            f"[vite_static] '{path}' not found in manifest.json. "
            "Make sure it's in Vite's build input and you ran `npm run build`."
        )
        raise KeyError(msg)

    # Return full static URL with hashed filename
    return f"{settings.STATIC_URL}{hashed['file']}"
