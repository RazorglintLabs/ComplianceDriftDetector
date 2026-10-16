"""Read-only bundled assets are separate from writable desktop output."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def resource_root() -> Path:
    """Root containing synthetic example CSVs in source or frozen Windows EXE."""
    if getattr(sys, "frozen", False):
        # Set by PyInstaller one-file extraction; never write customer reports here.
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent


def reports_dir() -> Path:
    """Only the frozen desktop changes where it writes generated reports."""
    if getattr(sys, "frozen", False):
        local = os.environ.get("LOCALAPPDATA")
        base = Path(local) if local else Path.home() / "AppData" / "Local"
        return base / "RazorglintLabs" / "ComplianceDriftDetector" / "output"
    return resource_root() / "output"
