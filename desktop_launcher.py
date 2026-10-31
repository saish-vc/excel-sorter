"""Windows desktop entry point for the bundled SheetSort application."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    """Start the packaged Streamlit app without exposing a command prompt."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = bundle_root / "sheetsort" / "app" / "main.py"
    if not app_path.is_file():
        raise RuntimeError("SheetSort application files are missing from this installation.")

    # Add bundle root to sys.path so imports work
    sys.path.insert(0, str(bundle_root))

    os.environ.setdefault("SHEETSORT_RECIPE_DB", str(Path.home() / "SheetSort" / "recipes.db"))
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false",
    ]
    from streamlit.web import cli as streamlit_cli

    raise SystemExit(streamlit_cli.main())


if __name__ == "__main__":
    main()
