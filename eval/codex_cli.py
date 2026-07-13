"""Locate the Codex CLI across supported desktop app layouts."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


APP_CANDIDATES = (
    Path("/Applications/ChatGPT.app/Contents/Resources/codex"),
    Path("/Applications/Codex.app/Contents/Resources/codex"),
)


def resolve_codex_cli() -> Path:
    configured = os.environ.get("CODEX_CLI")
    if configured:
        path = Path(configured).expanduser()
        if path.is_file():
            return path
        raise RuntimeError(f"CODEX_CLI does not point to a file: {path}")

    for path in APP_CANDIDATES:
        if path.is_file():
            return path

    executable = shutil.which("codex")
    if executable:
        return Path(executable)

    searched = ", ".join(str(path) for path in APP_CANDIDATES)
    raise RuntimeError(f"Codex CLI not found. Set CODEX_CLI or install it at one of: {searched}")
