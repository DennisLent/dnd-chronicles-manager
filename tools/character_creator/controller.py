"""Controller functions connecting UI events to model and logic."""

from __future__ import annotations

from typing import Dict

from .logic import derivations
from .model.state import Selections


def on_abilities_changed(model: Selections) -> Dict[str, int]:
    """Recompute ability modifiers and return updated ability scores."""
    abilities = model.abilities_base
    return {ab: derivations.ability_mod(score) for ab, score in abilities.items()}


def on_level_changed(model: Selections) -> int:
    """Return proficiency bonus for the model's level."""
    return derivations.prof_bonus(model.level)
