import json
import pathlib
import sys

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from srd_data import (
    CLASSES, RACES, SUBRACES, BACKGROUNDS,
    ABILITIES, SKILLS, CLASS_SKILL_CHOICES, CLASS_STARTING_EQUIPMENT,
    CLASS_HIT_DIE, CLASS_SAVE_THROWS, ALIGNMENTS, STANDARD_ARRAY,
    POINT_BUY_MIN, POINT_BUY_MAX, POINT_BUY_BUDGET, POINT_BUY_COST,
    DERIVED_RULES, CLASS_SPELLCASTING_ABILITY, SRD_SPELL_LISTS_MIN
)
from helpers import (
    ability_mod, prof_bonus, compute_skill_bonuses,
    validate_standard_array, point_buy_cost, within_point_buy_budget
)

# ---------------------------
# Utility
# ---------------------------

def desktop_default_path(filename: str) -> pathlib.Path:
    desk = pathlib.Path.home() / "Desktop"
    if desk.exists():
        return desk / filename
    return pathlib.Path.cwd() / filename


def default_character():
    return {
        "meta": {
            "name": "", "player": "",
            "race": "", "subrace": None,
            "class": "", "level": 1,
            "background": "", "alignment": "True Neutral"
        },
        "abilities": {a: 10 for a in ABILITIES},            # final (after ASI)
        "base_abilities": {a: 10 for a in ABILITIES},       # before racial ASI
        "race": {"features": [], "asi": {}, "speed": 30, "darkvision": 0, "languages": []},
        "class": {"save_throws": [], "hit_die": "1d8", "skill_choices": [], "equipment": []},
        "background": {"skills": [], "tools": [], "languages": [], "feature": "", "equipment": []},
        "skills": {},
        "hp": {"max": 8, "current": 8, "temporary": 0, "hit_die": "1d8"},
        "ac": 10, "speed": 30, "initiative": 0, "passive_perception": 10,
        "spells": {"casting_ability": "", "spell_save_dc": 0, "spell_attack_bonus": 0, "known": [], "slots": {}},
        "inventory": [],
        "languages": [],
        "notes": "",
        "appearance": {"Age": "", "Height": "", "Weight": "", "Eyes": "", "Skin": "", "Hair": ""},
        "personality": {"traits": [], "ideal": "", "bond": "", "flaw": ""}
    }


# ---------------------------
# Tkinter App
# ---------------------------
class CharacterCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DnD 5e Character Creator (Tk)")
        self.geometry("980x720")

        self.state_vars()
        self.build_ui()
        self.bind_events()
        self.refresh_all()

    # -----------------------
    # State / Model
    # -----------------------
    def state_vars(self):
        # Basics
        self.v_name = tk.StringVar()
        self.v_player = tk.StringVar()
        self.v_race = tk.StringVar()
        self.v_subrace = tk.StringVar()
        self.v_class = tk.StringVar()
        self.v_level = tk.IntVar(value=1)
        self.v_background = tk.StringVar()
        self.v_alignment = tk.StringVar(value="True Neutral")

        # Abilities method
        self.v_method = tk.StringVar(value="point")  # point | array | manual
        # Point-buy
        self.v_pb = {a: tk.IntVar(value=8) for a in ABILITIES}
        # Array
        self.v_arr = {a: tk.IntVar(value=0) for a in ABILITIES}  # store chosen value
        # Manual
        self.v_man = {a: tk.IntVar(value=10) for a in ABILITIES}

        # Skills prof checkboxes
        self.v_skill_prof = {sk: tk.BooleanVar(value=False) for sk in SKILLS}

        # Combat
        self.v_ac = tk.IntVar(value=10)
        self.v_speed = tk.IntVar(value=30)
        self.v_hp_max = tk.IntVar(value=8)
        self.v_hp_current = tk.IntVar(value=8)
        self.v_initiative = tk.StringVar(value="+0")
        self.v_pp = tk.StringVar(value="10")

        # Chosen spells
        self.chosen_spells = []

    # -----------------------
    # UI Construction
    # -----------------------
    def build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_basics = ttk.Frame(nb)
        self.tab_abilities = ttk.Frame(nb)
        self.tab_skills = ttk.Frame(nb)
        self.tab_background = ttk.Frame(nb)
        self.tab_combat = ttk.Frame(nb)
        self.tab_export = ttk.Frame(nb)

        nb.add(self.tab_basics, text="Basics")
        nb.add(self.tab_abilities, text="Abilities")
        nb.add(self.tab_skills, text="Skills & Equipment")
        nb.add(self.tab_background, text="Background & Details")
        nb.add(self.tab_combat, text="Combat & Spells")
        nb.add(self.tab_export, text="Export")

        self.build_basics()
        self.build_abilities()
        self.build_skills_equipment()
        self.build_background()
        self.build_combat_spells()
        self.build_export()

    def build_basics(self):
        frm = self.tab_basics
        # Row 1
        r1 = ttk.Frame(frm)
        r1.pack(fill=tk.X, pady=6)
        ttk.Label(r1, text="Character Name").pack(side=tk.LEFT)
        ttk.Entry(r1, textvariable=self.v_name, width=28).pack(side=tk.LEFT, padx=6)
        ttk.Label(r1, text="Player").pack(side=tk.LEFT)
        ttk.Entry(r1, textvariable=self.v_player, width=24).pack(side=tk.LEFT, padx=6)

        # Row 2
        r2 = ttk.Frame(frm)
        r2.pack(fill=tk.X, pady=6)
        ttk.Label(r2, text="Race").pack(side=tk.LEFT)
        self.cb_race = ttk.Combobox(r2, state="readonly", width=24, textvariable=self.v_race,
                                    values=sorted(RACES.keys()))
        self.cb_race.pack(side=tk.LEFT, padx=6)
        ttk.Label(r2, text="Subrace").pack(side=tk.LEFT)
        self.cb_subrace = ttk.Combobox(r2, state="readonly", width=24, textvariable=self.v_subrace, values=[])
        self.cb_subrace.pack(side=tk.LEFT, padx=6)

        # Race info box
        self.txt_race = tk.Text(frm, height=6, width=110, wrap=tk.WORD)
        self.txt_race.configure(state=tk.DISABLED)
        self.txt_race.pack(fill=tk.X, padx=2, pady=6)

        # Row 3
        r3 = ttk.Frame(frm)
        r3.pack(fill=tk.X, pady=6)
        ttk.Label(r3, text="Class").pack(side=tk.LEFT)
        self.cb_class = ttk.Combobox(r3, state="readonly", width=20, textvariable=self.v_class, values=CLASSES)
        self.cb_class.pack(side=tk.LEFT, padx=6)
        ttk.Label(r3, text="Level").pack(side=tk.LEFT)
        self.spn_level = tk.Spinbox(r3, from_=1, to=20, width=5, textvariable=self.v_level)
        self.spn_level.pack(side=tk.LEFT, padx=6)
        ttk.Label(r3, text="Background").pack(side=tk.LEFT)
        self.cb_background = ttk.Combobox(r3, state="readonly", width=24, textvariable=self.v_background,
                                          values=sorted(BACKGROUNDS.keys()))
        self.cb_background.pack(side=tk.LEFT, padx=6)
        ttk.Label(r3, text="Alignment").pack(side=tk.LEFT)
        self.cb_alignment = ttk.Combobox(r3, state="readonly", width=22, textvariable=self.v_alignment,
                                         values=ALIGNMENTS)
        self.cb_alignment.pack(side=tk.LEFT, padx=6)

        # Row 4 – class saves & hit die
        r4 = ttk.Frame(frm)
        r4.pack(fill=tk.X, pady=6)
        ttk.Label(r4, text="Class Saves:").pack(side=tk.LEFT)
        self.lbl_saves = ttk.Label(r4, text="—")
        self.lbl_saves.pack(side=tk.LEFT, padx=8)
        ttk.Label(r4, text="Hit Die:").pack(side=tk.LEFT)
        self.lbl_hitdie = ttk.Label(r4, text="1d8")
        self.lbl_hitdie.pack(side=tk.LEFT, padx=8)

    def build_abilities(self):
        frm = self.tab_abilities
        # Method radios
        r_method = ttk.Frame(frm)
        r_method.pack(fill=tk.X, pady=6)
        ttk.Label(r_method, text="Ability Generation Method").pack(anchor=tk.W)
        ttk.Radiobutton(r_method, text="Point‑Buy (27)", variable=self.v_method, value="point",
                        command=self.refresh_method_visibility).pack(side=tk.LEFT)
        ttk.Radiobutton(r_method, text="Standard Array", variable=self.v_method, value="array",
                        command=self.refresh_method_visibility).pack(side=tk.LEFT)
        ttk.Radiobutton(r_method, text="Manual", variable=self.v_method, value="manual",
                        command=self.refresh_method_visibility).pack(side=tk.LEFT)

        # Point-buy frame
        self.frm_point = ttk.LabelFrame(frm, text="Point‑Buy")
        self.frm_point.pack(fill=tk.X, padx=4, pady=4)
        self.pb_labels = {}
        for a in ABILITIES:
            row = ttk.Frame(self.frm_point)
            row.pack(anchor=tk.W)
            ttk.Label(row, text=a, width=4).pack(side=tk.LEFT)
            tk.Spinbox(row, from_=POINT_BUY_MIN, to=POINT_BUY_MAX, width=5, textvariable=self.v_pb[a],
                       command=self.refresh_point_buy).pack(side=tk.LEFT)
            ttk.Label(row, text="mod:").pack(side=tk.LEFT, padx=(8,2))
            lbl = ttk.Label(row, text="-1")
            lbl.pack(side=tk.LEFT)
            self.pb_labels[a] = lbl
        r_budget = ttk.Frame(self.frm_point)
        r_budget.pack(anchor=tk.W, pady=4)
        ttk.Label(r_budget, text="Budget Remaining:").pack(side=tk.LEFT)
        self.lbl_pb_budget = ttk.Label(r_budget, text=str(POINT_BUY_BUDGET))
        self.lbl_pb_budget.pack(side=tk.LEFT, padx=6)

        # Array frame
        self.frm_array = ttk.LabelFrame(frm, text="Standard Array (15,14,13,12,10,8)")
        self.frm_array.pack(fill=tk.X, padx=4, pady=4)
        self.arr_combos = {}
        for a in ABILITIES:
            row = ttk.Frame(self.frm_array)
            row.pack(anchor=tk.W)
            ttk.Label(row, text=a, width=4).pack(side=tk.LEFT)
            cb = ttk.Combobox(row, state="readonly", width=6, values=STANDARD_ARRAY)
            cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_array_status())
            cb.pack(side=tk.LEFT)
            self.arr_combos[a] = cb
        r_status = ttk.Frame(self.frm_array)
        r_status.pack(anchor=tk.W, pady=4)
        ttk.Label(r_status, text="Status:").pack(side=tk.LEFT)
        self.lbl_arr_status = ttk.Label(r_status, text="Unassigned")
        self.lbl_arr_status.pack(side=tk.LEFT, padx=6)

        # Manual frame
        self.frm_manual = ttk.LabelFrame(frm, text="Manual")
        self.frm_manual.pack(fill=tk.X, padx=4, pady=4)
        self.man_labels = {}
        for a in ABILITIES:
            row = ttk.Frame(self.frm_manual)
            row.pack(anchor=tk.W)
            ttk.Label(row, text=a, width=4).pack(side=tk.LEFT)
            tk.Spinbox(row, from_=1, to=20, width=5, textvariable=self.v_man[a], command=self.refresh_manual_mods).pack(side=tk.LEFT)
            ttk.Label(row, text="mod:").pack(side=tk.LEFT, padx=(8,2))
            lbl = ttk.Label(row, text="0")
            lbl.pack(side=tk.LEFT)
            self.man_labels[a] = lbl

        # ASI preview + Apply button
        row_apply = ttk.Frame(frm)
        row_apply.pack(fill=tk.X, pady=6)
        ttk.Button(row_apply, text="Apply Race ASI Now", command=self.apply_race_asi_and_preview).pack(side=tk.LEFT)
        ttk.Label(row_apply, text="(can re‑apply after changes)").pack(side=tk.LEFT, padx=6)

        r_previews = ttk.Frame(frm)
        r_previews.pack(fill=tk.BOTH, expand=True)
        self.txt_asi = tk.Text(r_previews, height=6, width=44, wrap=tk.WORD)
        self.txt_final = tk.Text(r_previews, height=6, width=44, wrap=tk.WORD)
        for t in (self.txt_asi, self.txt_final):
            t.configure(state=tk.DISABLED)
        self.txt_asi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        self.txt_final.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

    def build_skills_equipment(self):
        frm = self.tab_skills
        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=4)
        ttk.Label(top, text="Skill choices allowed:").pack(side=tk.LEFT)
        self.lbl_skill_allow = ttk.Label(top, text="0")
        self.lbl_skill_allow.pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="/ from list below").pack(side=tk.LEFT)

        # Scrollable skills
        sk_container = ttk.Frame(frm)
        sk_container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(sk_container, height=220)
        vsb = ttk.Scrollbar(sk_container, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.skill_checks = {}
        for sk, ab in SKILLS.items():
            row = ttk.Frame(inner)
            row.pack(anchor=tk.W)
            var = self.v_skill_prof[sk]
            cb = ttk.Checkbutton(row, text=f"{sk} ({ab})", variable=var, command=self.refresh_skill_mods)
            cb.pack(side=tk.LEFT)
            lbl = ttk.Label(row, text="+0")
            lbl.pack(side=tk.LEFT, padx=6)
            self.skill_checks[sk] = lbl

        # Equipment area
        ttk.Label(frm, text="Equipment choices (by class):").pack(anchor=tk.W, pady=(8,2))
        self.equip_frame = ttk.Frame(frm)
        self.equip_frame.pack(fill=tk.X)

    def build_background(self):
        frm = self.tab_background
        ttk.Label(frm, text="Background details:").pack(anchor=tk.W)
        self.txt_bg = tk.Text(frm, height=6, width=110, wrap=tk.WORD)
        self.txt_bg.configure(state=tk.DISABLED)
        self.txt_bg.pack(fill=tk.X, pady=4)

        row = ttk.Frame(frm)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Extra Languages (comma‑separated)").pack(side=tk.LEFT)
        self.ent_extra_lang = ttk.Entry(row, width=40)
        self.ent_extra_lang.pack(side=tk.LEFT, padx=6)

        ttk.Label(frm, text="Appearance/Personality (optional)").pack(anchor=tk.W, pady=(6,2))
        for label, key in (("Traits", "traits"),("Ideal","ideal"),("Bond","bond"),("Flaw","flaw")):
            r = ttk.Frame(frm)
            r.pack(fill=tk.X, pady=2)
            ttk.Label(r, text=label, width=8).pack(side=tk.LEFT)
            ent = ttk.Entry(r, width=60)
            ent.pack(side=tk.LEFT)
            setattr(self, f"ent_{key}", ent)

    def build_combat_spells(self):
        frm = self.tab_combat
        row1 = ttk.Frame(frm)
        row1.pack(fill=tk.X, pady=6)
        ttk.Label(row1, text="Armor Class").pack(side=tk.LEFT)
        tk.Spinbox(row1, from_=1, to=25, width=5, textvariable=self.v_ac).pack(side=tk.LEFT, padx=6)
        ttk.Label(row1, text="Speed").pack(side=tk.LEFT)
        tk.Spinbox(row1, from_=0, to=60, width=5, textvariable=self.v_speed).pack(side=tk.LEFT, padx=6)
        ttk.Label(row1, text="HP (Max)").pack(side=tk.LEFT)
        tk.Spinbox(row1, from_=1, to=300, width=6, textvariable=self.v_hp_max).pack(side=tk.LEFT, padx=6)
        ttk.Label(row1, text="Current").pack(side=tk.LEFT)
        tk.Spinbox(row1, from_=0, to=300, width=6, textvariable=self.v_hp_current).pack(side=tk.LEFT, padx=6)

        row2 = ttk.Frame(frm)
        row2.pack(fill=tk.X, pady=6)
        ttk.Label(row2, text="Initiative:").pack(side=tk.LEFT)
        ttk.Label(row2, textvariable=self.v_initiative).pack(side=tk.LEFT, padx=6)
        ttk.Label(row2, text="Passive Perception:").pack(side=tk.LEFT)
        ttk.Label(row2, textvariable=self.v_pp).pack(side=tk.LEFT, padx=6)

        # Features & Inventory
        lf = ttk.LabelFrame(frm, text="Features & Inventory")
        lf.pack(fill=tk.BOTH, expand=True, pady=6)
        ttk.Label(lf, text="Features (one per line)").pack(anchor=tk.W)
        self.txt_features = tk.Text(lf, height=5, width=100)
        self.txt_features.pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(lf, text="Inventory (one per line)").pack(anchor=tk.W)
        self.txt_inventory = tk.Text(lf, height=5, width=100)
        self.txt_inventory.pack(fill=tk.X, padx=2, pady=2)

        # Spells quick pick
        lf2 = ttk.LabelFrame(frm, text="Spells (quick pick)")
        lf2.pack(fill=tk.BOTH, expand=True, pady=6)
        ttk.Label(lf2, text="Known/Prepared (add from list below)").pack(anchor=tk.W)
        self.lst_spells = tk.Listbox(lf2, selectmode=tk.EXTENDED, height=6, width=40)
        self.lst_spells.pack(side=tk.LEFT, padx=4, pady=4)
        btn_add = ttk.Button(lf2, text="Add Selected Spells", command=self.add_spells)
        btn_add.pack(side=tk.LEFT, padx=6)
        ttk.Label(lf2, text="Chosen:").pack(side=tk.LEFT, padx=(10,2))
        self.lbl_chosen_spells = ttk.Label(lf2, text="—")
        self.lbl_chosen_spells.pack(side=tk.LEFT)

    def build_export(self):
        frm = self.tab_export
        ttk.Label(frm, text="Notes").pack(anchor=tk.W)
        self.txt_notes = tk.Text(frm, height=8, width=100)
        self.txt_notes.pack(fill=tk.X, pady=6)
        row = ttk.Frame(frm)
        row.pack(fill=tk.X)
        ttk.Button(row, text="Save JSON", command=self.save_json).pack(side=tk.LEFT)
        ttk.Label(row, text="Output:").pack(side=tk.LEFT, padx=8)
        self.lbl_outpath = ttk.Label(row, text="—", width=80)
        self.lbl_outpath.pack(side=tk.LEFT)

    # -----------------------
    # Event wiring
    # -----------------------
    def bind_events(self):
        self.cb_race.bind("<<ComboboxSelected>>", lambda e: (self.update_race_info(), self.apply_race_asi_and_preview(), self.compute_derived()))
        self.cb_subrace.bind("<<ComboboxSelected>>", lambda e: (self.apply_race_asi_and_preview(), self.compute_derived()))
        self.cb_class.bind("<<ComboboxSelected>>", lambda e: (self.update_class_dependent(), self.apply_race_asi_and_preview(), self.refresh_skill_mods(), self.compute_derived()))
        self.spn_level.config(command=lambda: (self.update_class_dependent(), self.refresh_skill_mods(), self.compute_derived()))
        self.cb_background.bind("<<ComboboxSelected>>", lambda e: self.update_background_box())

    # -----------------------
    # Refresh helpers
    # -----------------------
    def refresh_all(self):
        self.refresh_method_visibility()
        self.refresh_point_buy()
        self.refresh_array_status()
        self.refresh_manual_mods()
        self.update_race_info()
        self.update_class_dependent()
        self.refresh_skill_mods()
        self.apply_race_asi_and_preview()
        self.compute_derived()

    def refresh_method_visibility(self):
        mode = self.v_method.get()
        for w in (self.frm_point, self.frm_array, self.frm_manual):
            w.pack_forget()
        if mode == "point":
            self.frm_point.pack(fill=tk.X, padx=4, pady=4)
        elif mode == "array":
            self.frm_array.pack(fill=tk.X, padx=4, pady=4)
        else:
            self.frm_manual.pack(fill=tk.X, padx=4, pady=4)

    def refresh_point_buy(self):
        spent = 0
        for a in ABILITIES:
            val = int(self.v_pb[a].get())
            spent += POINT_BUY_COST.get(val, 999)
            self.pb_labels[a].configure(text=f"{ability_mod(val):+d}")
        rem = POINT_BUY_BUDGET - spent
        self.lbl_pb_budget.configure(text=str(rem), foreground=("red" if rem < 0 else "black"))

    def refresh_array_status(self):
        assigned = {a: int(self.arr_combos[a].get()) if self.arr_combos[a].get() else 0 for a in ABILITIES}
        self.lbl_arr_status.configure(text=("OK" if validate_standard_array(assigned) else "Incomplete"))

    def refresh_manual_mods(self):
        for a in ABILITIES:
            self.man_labels[a].configure(text=f"{ability_mod(int(self.v_man[a].get())):+d}")

    def current_abilities(self):
        mode = self.v_method.get()
        if mode == "point":
            return {a: int(self.v_pb[a].get()) for a in ABILITIES}
        if mode == "array":
            vals = {}
            for a in ABILITIES:
                try:
                    vals[a] = int(self.arr_combos[a].get())
                except ValueError:
                    vals[a] = 8
            return vals
        return {a: int(self.v_man[a].get()) for a in ABILITIES}

    def refresh_skill_mods(self):
        abil = self.current_abilities()
        profs = [sk for sk in SKILLS if self.v_skill_prof[sk].get()]
        bonuses = compute_skill_bonuses(abil, profs, int(self.v_level.get()))
        for sk, mod in bonuses.items():
            self.skill_checks[sk].configure(text=f"{mod:+d}")

    def update_class_dependent(self):
        cl = self.v_class.get()
        if not cl:
            self.lbl_saves.configure(text="—")
            self.lbl_hitdie.configure(text="—")
            self.lbl_skill_allow.configure(text="0")
            self.render_equip([])
            self.lst_spells.delete(0, tk.END)
            return
        saves = ", ".join(CLASS_SAVE_THROWS.get(cl, []))
        self.lbl_saves.configure(text=saves or "—")
        self.lbl_hitdie.configure(text=CLASS_HIT_DIE.get(cl, "—"))
        allow = CLASS_SKILL_CHOICES.get(cl, {"choose":0}).get("choose", 0)
        self.lbl_skill_allow.configure(text=str(allow))
        self.render_equip(CLASS_STARTING_EQUIPMENT.get(cl, []))
        self.lst_spells.delete(0, tk.END)
        for sp in SRD_SPELL_LISTS_MIN.get(cl, []):
            self.lst_spells.insert(tk.END, sp)

    def render_equip(self, eq_rows):
        for child in self.equip_frame.winfo_children():
            child.destroy()
        self.eq_vars = []
        for i, group in enumerate(eq_rows):
            v = tk.StringVar(value="")
            self.eq_vars.append(v)
            row = ttk.Frame(self.equip_frame)
            row.pack(fill=tk.X, pady=2)
            for choice in group:
                ttk.Radiobutton(row, text=choice, value=choice, variable=v).pack(side=tk.LEFT, padx=4)

    def update_race_info(self):
        race = self.v_race.get()
        self.cb_subrace.set("")
        self.cb_subrace.configure(values=[])
        self.txt_race.configure(state=tk.NORMAL)
        self.txt_race.delete("1.0", tk.END)
        if not race:
            self.txt_race.configure(state=tk.DISABLED)
            return
        rdata = RACES[race]
        desc_lines = [f"{race} — {rdata.get('description','')}",
                      f"Size: {rdata.get('size','?')}  Speed: {rdata.get('speed',0)}  Darkvision: {rdata.get('darkvision',0)} ft",
                      f"Languages: {', '.join(rdata.get('languages', []))}"]
        if rdata.get("features"):
            desc_lines.append("Features: " + "; ".join(rdata["features"]))
        if rdata.get("asi"):
            asi = ", ".join([f"{k}+{v}" for k,v in rdata["asi"].items() if k != "ANY"]) + ("; +1 to two different stats" if "ANY" in rdata["asi"] else "")
            desc_lines.append("ASI: " + asi)
        self.txt_race.insert(tk.END, "".join(desc_lines))
        self.txt_race.configure(state=tk.DISABLED)

        # subraces
        subs = list((rdata.get("subraces") or {}).keys()) or SUBRACES.get(race, [])
        self.cb_subrace.configure(values=subs)

    def apply_race_asi_and_preview(self):
        base = self.current_abilities()
        race = self.v_race.get()
        sub = self.v_subrace.get()
        rdata = RACES.get(race, {})
        final = base.copy()
        asi_lines = []
        asi = dict(rdata.get("asi", {}))
        # subrace extras
        sdata = None
        if rdata.get("subraces") and sub and sub in rdata["subraces"]:
            sdata = rdata["subraces"][sub]
            for k, v in sdata.get("asi", {}).items():
                asi[k] = asi.get(k, 0) + v
        # ANY handling (Half‑Elf)
        if "ANY" in asi:
            picks = ["DEX", "CON"] if ("DEX" in final and "CON" in final) else list(final.keys())[:2]
            for p in picks[:2]:
                final[p] += 1
                asi_lines.append(f"ANY +1 -> {p}")
        for stat, inc in asi.items():
            if stat == "ANY":
                continue
            final[stat] = int(final.get(stat, 0)) + int(inc)
            asi_lines.append(f"{stat} +{inc}")
        # write previews
        self._set_text(self.txt_asi, "Applied ASI:" + ("".join(asi_lines) if asi_lines else "(none)"))        
        final_text = "Final Abilities:" + ", ".join([f"{a} {final[a]} ({ability_mod(final[a]):+d})" for a in ABILITIES])
        self._set_text(self.txt_final, final_text)
        return base, final

    def compute_derived(self):
        _, final_abilities = self.apply_race_asi_and_preview()
        lvl = int(self.v_level.get())
        init = ability_mod(final_abilities["DEX"])
        self.v_initiative.set(f"{init:+d}")
        profs = [sk for sk in SKILLS if self.v_skill_prof[sk].get()]
        skills = compute_skill_bonuses(final_abilities, profs, lvl)
        self.v_pp.set(str(10 + int(skills.get("Perception", 0))))
        # HP L1 suggestion
        cl = self.v_class.get()
        hd = CLASS_HIT_DIE.get(cl, "1d8")
        try:
            die_max = int(hd.split("d")[1])
        except Exception:
            die_max = 8
        if lvl == 1:
            hp1 = max(1, die_max + ability_mod(final_abilities["CON"]))
            self.v_hp_max.set(hp1)
            self.v_hp_current.set(hp1)

    def update_background_box(self):
        bg = self.v_background.get()
        self._set_text(self.txt_bg, "")
        if not bg:
            return
        b = BACKGROUNDS[bg]
        lang_desc = b['languages'] if isinstance(b['languages'], int) else ", ".join(b['languages'])
        blines = [f"Skills: {', '.join(b['skills']) or '—'}",
                  f"Tools: {', '.join(b['tools']) or '—'}",
                  f"Languages: {lang_desc}",
                  f"Feature: {b['feature']}",
                  f"Equipment: {', '.join(b['equipment'])}"]
        self._set_text(self.txt_bg, "".join(blines))

    def add_spells(self):
        sels = [self.lst_spells.get(i) for i in self.lst_spells.curselection()]
        for p in sels:
            if p not in self.chosen_spells:
                self.chosen_spells.append(p)
        self.lbl_chosen_spells.configure(text=", ".join(self.chosen_spells) if self.chosen_spells else "—")

    def save_json(self):
        # Validate skill count
        cl = self.v_class.get()
        allow = CLASS_SKILL_CHOICES.get(cl, {"choose":0}).get("choose", 0)
        selected_skills = [sk for sk in SKILLS if self.v_skill_prof[sk].get()]
        if allow and len(selected_skills) > allow:
            messagebox.showerror("Error", f"You selected {len(selected_skills)} skills, but {cl} allows {allow}.")
            return

        # Build character object
        char = default_character()
        # Meta
        char["meta"]["name"] = self.v_name.get().strip()
        char["meta"]["player"] = self.v_player.get().strip()
        char["meta"]["race"] = self.v_race.get() or ""
        char["meta"]["subrace"] = self.v_subrace.get() or None
        char["meta"]["class"] = cl or ""
        char["meta"]["level"] = int(self.v_level.get() or 1)
        char["meta"]["background"] = self.v_background.get() or ""
        char["meta"]["alignment"] = self.v_alignment.get() or "True Neutral"

        # Abilities
        base, final_abilities = self.apply_race_asi_and_preview()
        char["base_abilities"].update(base)
        char["abilities"].update(final_abilities)

        # Race details
        rdata = RACES.get(char["meta"]["race"], {})
        sdata = (rdata.get("subraces", {}) or {}).get(char["meta"]["subrace"], {})
        char["race"]["features"] = (rdata.get("features") or []) + (sdata.get("features") or [])
        # Merge ASIs (py<3.9 friendly)
        base_asi = dict(rdata.get("asi", {}))
        base_asi.update(sdata.get("asi", {}))
        char["race"]["asi"] = base_asi
        char["race"]["speed"] = sdata.get("speed", rdata.get("speed", 30))
        char["race"]["darkvision"] = sdata.get("darkvision", rdata.get("darkvision", 0))
        char["race"]["languages"] = rdata.get("languages", [])
        char["speed"] = char["race"]["speed"]

        # Class details
        char["class"]["save_throws"] = CLASS_SAVE_THROWS.get(cl, [])
        char["class"]["hit_die"] = CLASS_HIT_DIE.get(cl, "1d8")
        char["class"]["skill_choices"] = selected_skills
        # Equipment picks (one per row)
        chosen_eq = []
        eq_rows = CLASS_STARTING_EQUIPMENT.get(cl, [])
        for var in getattr(self, "eq_vars", []):
            if var.get():
                chosen_eq.append(var.get())
        char["class"]["equipment"] = chosen_eq

        # Background
        bg = self.v_background.get()
        if bg:
            b = BACKGROUNDS[bg]
            char["background"]["skills"] = b.get("skills", [])
            char["background"]["tools"] = b.get("tools", [])
            langs = b.get("languages", 0)
            user_extra = [s.strip() for s in (self.ent_extra_lang.get() or "").split(",") if s.strip()]
            if isinstance(langs, int):
                char["background"]["languages"] = user_extra[:langs]
            else:
                char["background"]["languages"] = list(langs)
            char["background"]["feature"] = b.get("feature", "")
            char["background"]["equipment"] = b.get("equipment", [])
        char["languages"] = list(set((char["race"]["languages"] or []) + (char["background"]["languages"] or [])))

        # Skills
        char["skills"] = compute_skill_bonuses(final_abilities, selected_skills, char["meta"]["level"])

        # Combat deriveds
        char["hp"]["hit_die"] = char["class"]["hit_die"]
        if int(char["meta"]["level"]) == 1:
            try:
                die_max = int(char["class"]["hit_die"].split("d")[1])
            except Exception:
                die_max = 8
            char["hp"]["max"] = max(1, die_max + ability_mod(final_abilities["CON"]))
            char["hp"]["current"] = char["hp"]["max"]
        else:
            char["hp"]["max"] = int(self.v_hp_max.get())
            char["hp"]["current"] = int(self.v_hp_current.get())
        char["ac"] = int(self.v_ac.get())
        char["initiative"] = ability_mod(final_abilities["DEX"])
        char["passive_perception"] = 10 + int(char["skills"].get("Perception", 0))

        # Spells quick pick
        cl = self.v_class.get()
        if cl in CLASS_SPELLCASTING_ABILITY:
            cab = CLASS_SPELLCASTING_ABILITY[cl]
            char["spells"]["casting_ability"] = cab
            char["spells"]["spell_save_dc"] = 8 + prof_bonus(char["meta"]["level"]) + ability_mod(final_abilities[cab])
            char["spells"]["spell_attack_bonus"] = prof_bonus(char["meta"]["level"]) + ability_mod(final_abilities[cab])
            char["spells"]["known"] = list(self.chosen_spells)
        else:
            char["spells"] = {"casting_ability": "", "spell_save_dc": 0, "spell_attack_bonus": 0, "known": [], "slots": {}}

        # Features/Inventory/Notes
        char["features"] = [ln.strip() for ln in self.txt_features.get("1.0", tk.END).splitlines() if ln.strip()]
        char["inventory"] = [ln.strip() for ln in self.txt_inventory.get("1.0", tk.END).splitlines() if ln.strip()]
        char["notes"] = self.txt_notes.get("1.0", tk.END).strip()

        # Personality
        traits = getattr(self, "ent_traits", None).get() if hasattr(self, "ent_traits") else ""
        if traits:
            char["personality"]["traits"] = [t.strip() for t in traits.split(",") if t.strip()]
        char["personality"]["ideal"] = getattr(self, "ent_ideal", None).get() if hasattr(self, "ent_ideal") else ""
        char["personality"]["bond"] = getattr(self, "ent_bond", None).get() if hasattr(self, "ent_bond") else ""
        char["personality"]["flaw"] = getattr(self, "ent_flaw", None).get() if hasattr(self, "ent_flaw") else ""

        # Final validations
        errors = []
        if not char["meta"]["name"]: errors.append("Name is required.")
        if not char["meta"]["race"]: errors.append("Race is required.")
        if not char["meta"]["class"]: errors.append("Class is required.")
        if self.v_method.get() == "point" and not within_point_buy_budget(base):
            errors.append("Point‑buy budget exceeded.")
        if self.v_method.get() == "array":
            assigned = {a: int(self.arr_combos[a].get()) if self.arr_combos[a].get() else 0 for a in ABILITIES}
            if not validate_standard_array(assigned):
                errors.append("Standard array must be assigned exactly once (15,14,13,12,10,8).")
        if allow and len(selected_skills) != allow:
            errors.append(f"Select exactly {allow} class skills.")
        if errors:
            messagebox.showerror("Error", "".join(errors))
            return

        # File dialog
        base_filename = f"{char['meta']['name'].strip().replace(' ','_')}_character.json" or "character_character.json"
        suggested = desktop_default_path(base_filename)
        out_path = filedialog.asksaveasfilename(
            title="Save Character JSON",
            initialfile=suggested.name,
            initialdir=str(suggested.parent),
            defaultextension=".json",
            filetypes=[("JSON","*.json")]
        )
        if not out_path:
            return
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(char, f, indent=2)
            self.lbl_outpath.configure(text=out_path)
            messagebox.showinfo("Saved", f"Saved: {out_path}")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save file:{e}")

    # -----------------------
    # Helpers
    # -----------------------
    @staticmethod
    def _set_text(widget: tk.Text, content: str):
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.configure(state=tk.DISABLED)


if __name__ == "__main__":
    app = CharacterCreator()
    app.mainloop()
