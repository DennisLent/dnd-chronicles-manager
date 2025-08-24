from srd_data import ABILITIES, SKILLS, POINT_BUY_COST, POINT_BUY_BUDGET, STANDARD_ARRAY

def ability_mod(score: int) -> int:
    return (score - 10) // 2

def prof_bonus(level: int) -> int:
    if level >= 17: return 6
    if level >= 13: return 5
    if level >= 9:  return 4
    if level >= 5:  return 3
    return 2

def compute_skill_bonuses(abilities: Dict[str, int],
                          proficient_skills: Iterable[str],
                          level: int) -> Dict[str, int]:
    PB = prof_bonus(level)
    prof_set = set(proficient_skills)
    out = {}
    for sk, ab in SKILLS.items():
        mod = ability_mod(int(abilities[ab]))
        if sk in prof_set:
            mod += PB
        out[sk] = mod
    return out

def validate_standard_array(assignment: Dict[str, int]) -> bool:
    vals = sorted(int(assignment.get(a, 0)) for a in ABILITIES)
    return vals == sorted(STANDARD_ARRAY)

def point_buy_cost(assignment: Dict[str, int]) -> int:
    return sum(POINT_BUY_COST[int(assignment[a])] for a in ABILITIES)

def within_point_buy_budget(assignment: Dict[str, int]) -> bool:
    return point_buy_cost(assignment) <= POINT_BUY_BUDGET
