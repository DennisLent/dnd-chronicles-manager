import json
import pathlib
import PySimpleGUI as sg
from srd_data import (
    CLASSES, RACES, SUBRACES, ALIGNMENTS, ABILITIES, SKILLS,
    CLASS_HIT_DIE, CLASS_SAVE_THROWS,
    STANDARD_ARRAY, POINT_BUY_MIN, POINT_BUY_MAX,
    POINT_BUY_BUDGET, POINT_BUY_COST
)
from helpers import ability_mod, prof_bonus, compute_skill_bonuses


def default_character():
    return {
        "meta": {
            "name": "", "race": "", "subrace": None,
            "class": "", "subclass": None, "level": 1,
            "background": "", "alignment": "", "player": ""
        },
        "abilities": {a: 10 for a in ABILITIES},
        "proficiencies": {"saving_throws": [], "armor": [], "weapons": [], "tools": [], "languages": []},
        "skills": {},
        "hp": {"max": 8, "current": 8, "temporary": 0, "hit_die": "1d8"},
        "ac": 10, "speed": 30,
        "attacks": [], "features": [],
        "spells": {"casting_ability": "", "spell_save_dc": 0, "spell_attack_bonus": 0, "known": [], "slots": {}},
        "inventory": [],
        "notes": ""
    }

# ---------------------------
# GUI: layout
# ---------------------------
sg.theme("DarkBlue3")

# ---- Basics tab ----
RACE_LIST = list(RACES.keys())

def make_basics_tab():
    return [
        [sg.Text("Character Name"), sg.Input(key="name", size=(28,1))],
        [sg.Text("Player"), sg.Input(key="player", size=(20,1)), sg.Text("Background"), sg.Input(key="background", size=(20,1))],
        [sg.Text("Race"), sg.Combo(RACE_LIST, key="race", size=(22,1), readonly=True, enable_events=True)],
        [sg.Text("Subrace", key="subrace_label", visible=False),
         sg.Combo([], key="subrace", size=(24,1), readonly=True, enable_events=True, visible=False)],
        [sg.Text("Class"), sg.Combo(CLASSES, key="class", size=(22,1), readonly=True, enable_events=True),
         sg.Text("Level"), sg.Spin([i for i in range(1,21)], initial_value=1, key="level", size=(5,1), enable_events=True)],
        [sg.Text("Alignment"), sg.Combo(ALIGNMENTS, key="alignment", size=(22,1), readonly=True)],
        [sg.Text("Proficiency Bonus:"), sg.Text("+2", key="profbonus", size=(4,1))],
        [sg.Frame("Race & Subrace Info", [[sg.Multiline(key="race_info", size=(70,6), disabled=True)],
                                           [sg.Multiline(key="subrace_info", size=(70,4), disabled=True)]], expand_x=True)]
    ]

# ---- Abilities tab ----
POINT_BUY_HELP = f"Point-Buy: budget {POINT_BUY_BUDGET}; scores {POINT_BUY_MIN}-{POINT_BUY_MAX}."

def make_abilities_tab():
    method_row = [
        [sg.Text("Ability Generation Method:"), sg.Text(POINT_BUY_HELP)],
        [sg.Radio("Point-Buy (27)", "METHOD", key="m_point", default=True, enable_events=True),
         sg.Radio("Standard Array", "METHOD", key="m_array", enable_events=True),
         sg.Radio("Manual", "METHOD", key="m_manual", enable_events=True)],
    ]

    # point-buy controls
    pb_rows = []
    for a in ABILITIES:
        pb_rows.append([sg.Text(a, size=(4,1)),
                        sg.Spin([i for i in range(POINT_BUY_MIN, POINT_BUY_MAX+1)], initial_value=8, key=f"pb_{a}", enable_events=True, size=(5,1)),
                        sg.Text("mod:"), sg.Text("-1", key=f"pbm_{a}", size=(3,1))])
    point_buy_layout = [[sg.Frame("Point-Buy Scores", pb_rows)],
                        [sg.Text("Budget Remaining:"), sg.Text(str(POINT_BUY_BUDGET), key="pb_budget")]]

    # standard array
    arr_rows = []
    for a in ABILITIES:
        arr_rows.append([sg.Text(a, size=(4,1)), sg.Combo(STANDARD_ARRAY, key=f"arr_{a}", readonly=True, enable_events=True, size=(5,1))])
    array_layout = [[sg.Text("Assign each value once: 15, 14, 13, 12, 10, 8")], *arr_rows,
                    [sg.Text("Status:"), sg.Text("Unassigned", key="arr_status")]]

    # manual
    man_rows = []
    for a in ABILITIES:
        man_rows.append([sg.Text(a, size=(4,1)),
                         sg.Spin([i for i in range(1,21)], initial_value=10, key=f"man_{a}", enable_events=True, size=(5,1)),
                         sg.Text("mod:"), sg.Text("0", key=f"manm_{a}")])
    manual_layout = [sg.Frame("Manual Scores", man_rows)]

    return method_row + [
        [sg.Column(point_buy_layout, key="col_point")],
        [sg.Column(array_layout, key="col_array", visible=False)],
        [sg.Column(manual_layout, key="col_manual", visible=False)],
    ]

# ---- Proficiencies & Skills tab ----

def make_profs_tab():
    skill_rows = []
    for sk, ab in SKILLS.items():
        skill_rows.append([sg.Checkbox(sk, key=f"skprof_{sk}", enable_events=True),
                           sg.Text(f"({ab})"), sg.Text("+0", key=f"skmod_{sk}", size=(4,1))])
    return [
        [sg.Text("Saving Throw Proficiencies (from Class):"), sg.Text("—", key="savethrows")],
        [sg.Frame("Skill Proficiencies", [[sg.Column(skill_rows, scrollable=True, size=(380,220))]])],
    ]

# ---- Combat & Gear tab ----

def make_combat_tab():
    return [
        [sg.Text("Armor Class"), sg.Spin([i for i in range(1,26)], initial_value=10, key="ac", size=(5,1)),
         sg.Text("Speed"), sg.Spin([i for i in range(0,61)], initial_value=30, key="speed", size=(5,1))],
        [sg.Text("Hit Die"), sg.Input(default_text="1d8", key="hit_die", size=(8,1)),
         sg.Text("Max HP (lvl1 tip: max die + CON mod)"), sg.Spin([i for i in range(1,300)], initial_value=8, key="hp_max", size=(5,1)),
         sg.Text("Current HP"), sg.Spin([i for i in range(0,300)], initial_value=8, key="hp_current", size=(5,1))],
        [sg.Text("Features & Traits (one per line)")],
        [sg.Multiline(key="features", size=(70,5))],
        [sg.Text("Inventory (one per line)")],
        [sg.Multiline(key="inventory", size=(70,5))],
    ]

# ---- Notes & Export tab ----

def make_export_tab():
    return [
        [sg.Text("Notes")],
        [sg.Multiline(key="notes", size=(70,8))],
        [sg.Button("Save JSON", key="save"), sg.Text("Output path:"), sg.Text("—", key="outpath")]
    ]

# Compose window
layout = [[sg.TabGroup([[
    sg.Tab("Basics", make_basics_tab()),
    sg.Tab("Abilities", make_abilities_tab()),
    sg.Tab("Proficiencies & Skills", make_profs_tab()),
    sg.Tab("Combat & Gear", make_combat_tab()),
    sg.Tab("Notes & Export", make_export_tab()),
]])]]

window = sg.Window("DnD 5e Character Creator", layout, finalize=True)
values = window.read(timeout=0)[1]

# ---------------------------
# Dynamic update helpers
# ---------------------------

def refresh_prof_bonus(v):
    window["profbonus"].update(f"+{prof_bonus(int(v.get("level", 1)))}")


def refresh_saves(v):
    cl = v.get("class")
    saves = CLASS_SAVE_THROWS.get(cl, [])
    window["savethrows"].update(", ".join(saves) if saves else "—")


def refresh_hit_die_and_hp(v):
    cl = v.get("class")
    if not cl:
        return
    hd = CLASS_HIT_DIE.get(cl, "1d8")
    window["hit_die"].update(hd)
    try:
        die_max = int(hd.split("d")[1])
    except Exception:
        die_max = 8
    con_mod = ability_mod(current_abilities(v)["CON"])
    if int(v.get("level", 1)) == 1:
        suggested = max(1, die_max + con_mod)
        window["hp_max"].update(suggested)
        window["hp_current"].update(suggested)


def refresh_point_buy(v):
    spent = 0
    for a in ABILITIES:
        val = int(v[f"pb_{a}"])
        spent += POINT_BUY_COST.get(val, 999)
        window[f"pbm_{a}"].update(f"{ability_mod(val):+d}")
    rem = POINT_BUY_BUDGET - spent
    window["pb_budget"].update(str(rem), text_color=("red" if rem < 0 else "white"))


def refresh_array_status(v):
    chosen = [v.get(f"arr_{a}") for a in ABILITIES]
    ok = sorted([c for c in chosen if c is not None]) == sorted(STANDARD_ARRAY)
    window["arr_status"].update("OK" if ok else "Incomplete")


def refresh_manual_mods(v):
    for a in ABILITIES:
        window[f"manm_{a}"].update(f"{ability_mod(int(v[f'man_{a}'])):+d}")


def refresh_skill_mods(v):
    abil = current_abilities(v)
    profs = [sk for sk in SKILLS if v.get(f"skprof_{sk}")]
    bonuses = compute_skill_bonuses(abil, profs, int(v.get("level", 1)))
    for sk, mod in bonuses.items():
        window[f"skmod_{sk}"].update(f"{mod:+d}")


def show_race_and_subrace_info(v):
    race = v.get("race")
    # Race description
    if race:
        window["race_info"].update(RACES.get(race, ""))
    else:
        window["race_info"].update("")
    # Subrace options + description
    opts = []
    sub_desc = ""
    if race and race in SUBRACES:
        # SUBRACES is dict[race] -> {subrace: description}
        sub_map = SUBRACES[race]
        opts = list(sub_map.keys())
        chosen = v.get("subrace") if v.get("subrace") in opts else None
        window["subrace"].update(values=opts, value=chosen, visible=True)
        window["subrace_label"].update(visible=True)
        if chosen:
            sub_desc = sub_map.get(chosen, "")
    else:
        window["subrace"].update(values=[], value=None, visible=False)
        window["subrace_label"].update(visible=False)
    window["subrace_info"].update(sub_desc)


def current_abilities(v) -> dict:
    if v.get("m_point"):
        return {a: int(v[f"pb_{a}"]) for a in ABILITIES}
    if v.get("m_array"):
        return {a: int(v.get(f"arr_{a}") or 8) for a in ABILITIES}
    return {a: int(v[f"man_{a}"]) for a in ABILITIES}

# initial refresh
refresh_prof_bonus(values)
refresh_saves(values)
refresh_hit_die_and_hp(values)
refresh_point_buy(values)
refresh_array_status(values)
refresh_manual_mods(values)
refresh_skill_mods(values)
show_race_and_subrace_info(values)

# ---------------------------
# Event loop
# ---------------------------
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, None):
        break

    if event == "race":
        show_race_and_subrace_info(values)

    if event == "subrace":
        show_race_and_subrace_info(values)

    if event in ("m_point", "m_array", "m_manual"):
        window["col_point"].update(visible=values.get("m_point"))
        window["col_array"].update(visible=values.get("m_array"))
        window["col_manual"].update(visible=values.get("m_manual"))
        refresh_skill_mods(values)
        refresh_hit_die_and_hp(values)

    if event in ("level", "class"):
        refresh_prof_bonus(values)
        refresh_saves(values)
        refresh_hit_die_and_hp(values)
        refresh_skill_mods(values)

    if isinstance(event, str) and event.startswith("pb_"):
        refresh_point_buy(values)
        refresh_skill_mods(values)
        refresh_hit_die_and_hp(values)

    if isinstance(event, str) and event.startswith("arr_"):
        refresh_array_status(values)
        refresh_skill_mods(values)
        refresh_hit_die_and_hp(values)

    if isinstance(event, str) and event.startswith("man_"):
        refresh_manual_mods(values)
        refresh_skill_mods(values)
        refresh_hit_die_and_hp(values)

    if isinstance(event, str) and event.startswith("skprof_"):
        refresh_skill_mods(values)

    if event == "save":
        char = default_character()
        # meta
        char["meta"]["name"] = values.get("name"," ").strip()
        char["meta"]["player"] = values.get("player"," ").strip()
        char["meta"]["race"] = values.get("race") or ""
        char["meta"]["subrace"] = values.get("subrace") or None
        char["meta"]["class"] = values.get("class") or ""
        char["meta"]["level"] = int(values.get("level", 1))
        char["meta"]["background"] = values.get("background"," ").strip()
        char["meta"]["alignment"] = values.get("alignment") or ""

        # abilities
        abil = current_abilities(values)
        char["abilities"].update(abil)

        # proficiencies
        char["proficiencies"]["saving_throws"] = CLASS_SAVE_THROWS.get(char["meta"]["class"], [])

        # skills
        profs = [sk for sk in SKILLS if values.get(f"skprof_{sk}")]
        char["skills"] = compute_skill_bonuses(abil, profs, char["meta"]["level"])

        # combat & gear
        char["ac"] = int(values.get("ac", 10))
        char["speed"] = int(values.get("speed", 30))
        char["hp"]["hit_die"] = values.get("hit_die", "1d8")
        char["hp"]["max"] = int(values.get("hp_max", 1))
        char["hp"]["current"] = int(values.get("hp_current", 0))

        feats = [ln.strip() for ln in (values.get("features") or "").splitlines() if ln.strip()]
        inv = [ln.strip() for ln in (values.get("inventory") or "").splitlines() if ln.strip()]
        char["features"] = feats
        char["inventory"] = inv
        char["notes"] = values.get("notes","")

        # basic validations
        errors = []
        if not char["meta"]["name"]: errors.append("Name is required.")
        if not char["meta"]["race"]: errors.append("Race is required.")
        if not char["meta"]["class"]: errors.append("Class is required.")
        if values.get("m_point"):
            spent = sum(POINT_BUY_COST[int(values[f"pb_{a}"])] for a in ABILITIES)
            if spent > POINT_BUY_BUDGET:
                errors.append("Point-buy budget exceeded.")
        if values.get("m_array"):
            chosen = [values.get(f"arr_{a}") for a in ABILITIES]
            ok = sorted([c for c in chosen if c is not None]) == sorted(STANDARD_ARRAY)
            if not ok:
                errors.append("Standard array must be assigned once each (15,14,13,12,10,8).")

        if errors:
            sg.popup_error("\n".join(errors))
            continue

        fname = (char["meta"]["name"] or "character").replace(" ", "_")
        out = pathlib.Path.cwd() | pathlib.Path(f"{fname}.character.json")
        try:
            # pathlib '|' requires Python 3.11+; fallback if needed
            if not isinstance(out, pathlib.Path):
                out = pathlib.Path.cwd() / f"{fname}.character.json"
            with open(out, "w", encoding="utf-8") as f:
                json.dump(char, f, indent=2)
            window["outpath"].update(str(out))
            sg.popup_ok(f"Saved: {out}")
        except Exception as e:
            sg.popup_error(f"Failed to save file:\n{e}")

window.close()
