import sys, pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from tools.character_creator.logic import derivations, validators
from tools.character_creator.srd_data import ABILITIES, CLASS_HIT_DIE


def test_point_buy_cost_and_budget():
    assignment = {a: 8 for a in ABILITIES}
    assignment.update({"STR": 15, "DEX": 15, "CON": 15, "INT": 14})
    errors = validators.validate_point_buy(assignment)
    assert errors  # exceeds budget
    assignment = {a: 8 for a in ABILITIES}
    assignment.update({"STR": 15, "DEX": 15})
    errors = validators.validate_point_buy(assignment)
    assert not errors


def test_standard_array_assignment():
    assignment = dict(zip(ABILITIES, [15, 14, 13, 12, 10, 8]))
    assert not validators.validate_standard_array(assignment)
    bad = dict(zip(ABILITIES, [15, 14, 13, 12, 11, 7]))
    assert validators.validate_standard_array(bad)


def test_skill_bonus_math():
    abilities = {a: 10 for a in ABILITIES}
    abilities["DEX"] = 16  # mod +3
    bonuses = derivations.compute_skill_bonuses(abilities, ["Stealth"], level=1)
    assert bonuses["Stealth"] == 5  # +3 DEX +2 proficiency


def test_hp_level1_each_class():
    for klass, die in CLASS_HIT_DIE.items():
        die_value = int(die[2:])
        hp = derivations.compute_hp_level1(klass, con_mod=1)
        assert hp == die_value + 1


def test_half_elf_any_plus_one():
    base = {a: 10 for a in ABILITIES}
    asi = {"STR": 1, "DEX": 1}
    out = derivations.apply_asi(base, asi)
    assert out["STR"] == 11 and out["DEX"] == 11
