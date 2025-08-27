"""Helpers for serializing characters to and from JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

from ..model.state import Character, Selections


def build_character(model: Selections, derived: Dict[str, Any]) -> Character:
    """Combine user selections and derived data into a Character."""
    return Character(selections=model, data=derived)


def save_character(path: Path | str, char: Character) -> None:
    data = char.to_dict()
    data["schema_version"] = 1
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)


def load_character(path: Path | str) -> Character:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    selections = Selections(**data.pop("selections"))
    return Character(selections=selections, data=data)


def sanitize_filename(name: str) -> str:
    """Return a safe filename derived from ``name``."""
    base = re.sub(r"[^A-Za-z0-9_-]", "_", name.strip()) or "character"
    if not base.endswith("_character"):
        base += "_character"
    return base + ".json"
