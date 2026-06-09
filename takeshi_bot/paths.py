from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
ASSETS_DIR = PROJECT_ROOT / "assets"
TEMP_DIR = ASSETS_DIR / "temp"
AUTH_DIR = ASSETS_DIR / "auth" / "baileys"
COMMANDS_DIR = Path(__file__).resolve().parent / "commands"
BRIDGE_DIR = PROJECT_ROOT / "bridge"
BRIDGE_SCRIPT = BRIDGE_DIR / "baileys-sidecar.js"


def ensure_runtime_dirs() -> None:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
