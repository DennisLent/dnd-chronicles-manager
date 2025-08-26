"""Deprecated helpers kept for backward compatibility.

These functions are thin wrappers around the new logic modules.
"""

from __future__ import annotations

from .logic.derivations import ability_mod, prof_bonus, compute_skill_bonuses
from .logic.validators import (
    validate_standard_array,
    validate_point_buy,
    validate_skill_count,
)

__all__ = [
    "ability_mod",
    "prof_bonus",
    "compute_skill_bonuses",
    "validate_standard_array",
    "validate_point_buy",
    "validate_skill_count",
]
