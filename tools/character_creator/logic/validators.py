"""Validation rules for character creation inputs."""

from __future__ import annotations

from typing import Dict, Iterable, List

from ..srd_data import (
    ABILITIES,
    CLASS_SKILL_CHOICES,
    POINT_BUY_BUDGET,
    POINT_BUY_COST,
    POINT_BUY_MIN,
    POINT_BUY_MAX,
    STANDARD_ARRAY,
)


def validate_point_buy(abilities: Dict[str, int]) -> List[str]:
    errors: List[str] = []
    total = 0
    for ab in ABILITIES:
        score = int(abilities.get(ab, 0))
        if score < POINT_BUY_MIN or score > POINT_BUY_MAX:
            errors.append(
                f"{ab} must be between {POINT_BUY_MIN} and {POINT_BUY_MAX}"
            )
        total += POINT_BUY_COST[int(score)]
    if total > POINT_BUY_BUDGET:
        errors.append(
            f"Point-buy budget exceeded ({total}/{POINT_BUY_BUDGET})"
        )
    return errors


def validate_standard_array(assignment: Dict[str, int]) -> List[str]:
    vals = sorted(int(assignment.get(a, 0)) for a in ABILITIES)
    if vals != sorted(STANDARD_ARRAY):
        return ["Ability scores must match the standard array"]
    return []


def validate_skill_count(klass: str, profs: Iterable[str]) -> List[str]:
    info = CLASS_SKILL_CHOICES.get(klass)
    if not info:
        return []
    choose = info["choose"]
    profs_list = list(profs)
    errors: List[str] = []
    if len(profs_list) != choose:
        errors.append(f"Choose exactly {choose} skills for {klass}")
    invalid = [p for p in profs_list if p not in info["from"]]
    if invalid:
        errors.append(
            "Invalid skill selections: " + ", ".join(sorted(invalid))
        )
    return errors
