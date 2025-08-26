"""Helpers for serializing characters to and from JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from ..model.state import Character, Selections


def build_character(model: Selections, derived: Dict[str, Any]) -> Character:
    """Combine user selections and derived data into a Character."""
    return Character(selections=model, **derived)


def save_character(path: Path | str, char: Character) -> None:
    data = char.to_dict()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def load_character(path: Path | str) -> Character:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    selections = Selections(**data.pop("selections"))
    return Character(selections=selections, **data)
