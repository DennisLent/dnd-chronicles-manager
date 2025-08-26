"""Pure functions for computing derived character statistics."""

from __future__ import annotations

from typing import Dict, Iterable

from ..srd_data import ABILITIES, CLASS_HIT_DIE, SKILLS


def ability_mod(score: int) -> int:
    return (score - 10) // 2


def prof_bonus(level: int) -> int:
    if level >= 17:
        return 6
    if level >= 13:
        return 5
    if level >= 9:
        return 4
    if level >= 5:
        return 3
    return 2


def apply_asi(base: Dict[str, int], asi: Dict[str, int]) -> Dict[str, int]:
    out = dict(base)
    for ab, inc in asi.items():
        out[ab] = out.get(ab, 0) + inc
    return out


def compute_skill_bonuses(
    abilities: Dict[str, int],
    proficient_skills: Iterable[str],
    level: int,
) -> Dict[str, int]:
    pb = prof_bonus(level)
    prof_set = set(proficient_skills)
    bonuses: Dict[str, int] = {}
    for skill, ability in SKILLS.items():
        mod = ability_mod(int(abilities[ability]))
        if skill in prof_set:
            mod += pb
        bonuses[skill] = mod
    return bonuses


def compute_initiative(abilities: Dict[str, int]) -> int:
    return ability_mod(int(abilities["DEX"]))


def compute_hp_level1(klass: str, con_mod: int) -> int:
    die = CLASS_HIT_DIE.get(klass, "1d8")
    die_value = int(die.split("d")[-1])
    return die_value + con_mod
