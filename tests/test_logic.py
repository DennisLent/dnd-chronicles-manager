import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest

from tools.character_creator.logic.validators import (
    validate_point_buy,
    validate_standard_array,
    validate_skill_count,
)
from tools.character_creator.logic.derivations import (
    apply_asi,
    compute_skill_bonuses,
    compute_initiative,
    compute_hp_level1,
    prof_bonus,
)
from tools.character_creator.srd_data import (
    ABILITIES,
    CLASS_SKILL_CHOICES,
    FULL_CASTER_SLOTS,
    HALF_CASTER_LEVEL_MAP,
    WARLOCK_PACT_SLOTS,
)


def test_point_buy_validation():
    abilities = {ab: 8 for ab in ABILITIES}
    abilities["STR"] = 15
    abilities["DEX"] = 15
    assert validate_point_buy(abilities) == []
    bad = {ab: 15 for ab in ABILITIES}
    assert any("budget" in e for e in validate_point_buy(bad))


def test_standard_array_validation():
    assignment = {ab: val for ab, val in zip(ABILITIES, [15, 14, 13, 12, 10, 8])}
    assert validate_standard_array(assignment) == []
    wrong = assignment.copy()
    wrong["STR"] = 16
    assert validate_standard_array(wrong)


def test_apply_asi_and_skills():
    base = {ab: 10 for ab in ABILITIES}
    asi = {"STR": 2, "DEX": 1}
    final = apply_asi(base, asi)
    assert final["STR"] == 12 and final["DEX"] == 11
    skills = compute_skill_bonuses(final, ["Perception"], level=1)
    assert skills["Perception"] == 2  # WIS mod 0 + prof 2


def test_derived_stats():
    abilities = {"STR": 10, "DEX": 14, "CON": 12, "INT": 10, "WIS": 10, "CHA": 10}
    assert compute_initiative(abilities) == 2
    assert compute_hp_level1("Fighter", 1) == 11
    assert prof_bonus(1) == 2


def test_skill_count_validator():
    info = CLASS_SKILL_CHOICES["Fighter"]
    picks = info["from"][: info["choose"]]
    assert validate_skill_count("Fighter", picks) == []
    assert validate_skill_count("Fighter", picks + ["Arcana"])


def test_spell_slot_tables():
    assert FULL_CASTER_SLOTS[1][0] == 2
    assert HALF_CASTER_LEVEL_MAP[2] == 1
    assert WARLOCK_PACT_SLOTS[3] == (2, 2)
