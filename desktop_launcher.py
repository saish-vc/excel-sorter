"""Windows desktop entry point for the bundled SheetSort application."""
from __future__ import annotations

import os
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

# CRITICAL FOR PYINSTALLER:
# Streamlit defaults global.developmentMode to True if "site-packages" is not in __file__.
# In developmentMode, Streamlit expects a React dev server on port 3000, rejects server.port,
# and fails to serve static assets. We MUST force developmentMode to False!
os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
os.environ["STREAMLIT_SERVER_ADDRESS"] = "127.0.0.1"


def _patch_streamlit_static() -> None:
    """Ensure Streamlit can locate its static web assets in frozen bundles."""
    try:
        import streamlit.file_util as st_file_util

        bundle_root = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidates = [
            bundle_root / "_internal" / "streamlit" / "static",
            bundle_root / "streamlit" / "static",
            bundle_root / "_internal" / "static",
            bundle_root / "static",
            Path(st_file_util.__file__).resolve().parent / "static",
        ]

        for candidate in candidates:
            if (candidate / "index.html").is_file():
                resolved = str(candidate.resolve())
                st_file_util.get_static_dir = lambda: resolved
                os.environ["STREAMLIT_STATIC_DIR"] = resolved
                break
    except Exception as e:
        print(f"Warning: could not patch streamlit static assets: {e}")


def _open_browser_when_ready(url: str = "http://127.0.0.1:8501") -> None:
    """Poll the local server until it responds, then automatically open the browser."""
    for _ in range(60):
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    webbrowser.open(url)
                    return
        except Exception:
            time.sleep(0.5)
    webbrowser.open(url)


def main() -> None:
    """Start the packaged Streamlit app as a desktop application."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    app_path = bundle_root / "sheetsort" / "app" / "main.py"
    if not app_path.is_file():
        app_path = bundle_root / "_internal" / "sheetsort" / "app" / "main.py"
    if not app_path.is_file():
        app_path = Path(__file__).resolve().parent / "sheetsort" / "app" / "main.py"

    if not app_path.is_file():
        raise RuntimeError(f"SheetSort application files not found at: {app_path}")

    # Add bundle roots to sys.path
    for p in [bundle_root, bundle_root / "_internal", Path(__file__).resolve().parent]:
        p_str = str(p)
        if p_str not in sys.path:
            sys.path.insert(0, p_str)

    # Ensure recipe storage directory exists in user profile
    recipe_dir = Path.home() / "SheetSort"
    recipe_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SHEETSORT_RECIPE_DB", str(recipe_dir / "recipes.db"))

    # Patch static assets location
    _patch_streamlit_static()

    # Start background thread to open default browser once server responds
    threading.Thread(target=_open_browser_when_ready, args=("http://127.0.0.1:8501",), daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.address=127.0.0.1",
        "--server.port=8501",
        "--browser.gatherUsageStats=false",
    ]
    from streamlit.web import cli as streamlit_cli
    raise SystemExit(streamlit_cli.main())


if __name__ == "__main__":
    main()
