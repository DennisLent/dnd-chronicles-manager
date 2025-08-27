"""Tkinter screens for the character creator."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List

from ..config.text import HELP
from ..model.state import Selections
from ..srd_data import (
    ABILITIES,
    ALIGNMENTS,
    BACKGROUNDS,
    CLASSES,
    RACES,
    SUBRACES,
    CLASS_HIT_DIE,
    CLASS_SAVE_THROWS,
    CLASS_SKILL_CHOICES,
    CLASS_STARTING_EQUIPMENT,
    CLASS_SPELLCASTING_ABILITY,
    SRD_SPELL_LISTS_MIN,
    FULL_CASTER_SLOTS,
    HALF_CASTER_LEVEL_MAP,
    WARLOCK_PACT_SLOTS,
)
from ..logic.derivations import (
    apply_asi,
    prof_bonus,
    compute_skill_bonuses,
    compute_initiative,
    compute_hp_level1,
    ability_mod,
)
from ..logic.validators import (
    validate_skill_count,
    validate_point_buy,
    validate_standard_array,
)

ALL_LANGUAGES = sorted({lang for r in RACES.values() for lang in r.get("languages", [])})
from .widgets import HelpBanner, LabeledNumber


class BasicsScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model

        self.grid_columnconfigure(1, weight=1)

        # Player name first
        ttk.Label(self, text="Player:").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.var_player = tk.StringVar(value=self.model.player)
        ent_player = ttk.Entry(self, textvariable=self.var_player)
        ent_player.grid(row=0, column=1, sticky="ew", padx=4, pady=2)
        self.var_player.trace_add(
            "write", lambda *_: setattr(self.model, "player", self.var_player.get())
        )

        # Character name
        ttk.Label(self, text="Character Name:").grid(
            row=1, column=0, sticky="w", padx=4, pady=2
        )
        self.var_name = tk.StringVar(value=self.model.name)
        ent_name = ttk.Entry(self, textvariable=self.var_name)
        ent_name.grid(row=1, column=1, sticky="ew", padx=4, pady=2)
        self.var_name.trace_add(
            "write", lambda *_: setattr(self.model, "name", self.var_name.get())
        )

        # Race selection
        ttk.Label(self, text="Race:").grid(row=2, column=0, sticky="w", padx=4, pady=2)
        self.var_race = tk.StringVar(value=self.model.race)
        self.cb_race = ttk.Combobox(
            self, textvariable=self.var_race, values=sorted(RACES.keys()), state="readonly"
        )
        self.cb_race.grid(row=2, column=1, sticky="ew", padx=4, pady=2)
        self.var_race.trace_add("write", self._on_race_change)

        # Subrace selection
        ttk.Label(self, text="Subrace:").grid(row=3, column=0, sticky="w", padx=4, pady=2)
        self.var_sub = tk.StringVar(value=self.model.subrace or "")
        self.cb_sub = ttk.Combobox(self, textvariable=self.var_sub, state="disabled")
        self.cb_sub.grid(row=3, column=1, sticky="ew", padx=4, pady=2)
        self.var_sub.trace_add("write", self._on_subrace_change)

        # Class selection
        ttk.Label(self, text="Class:").grid(row=4, column=0, sticky="w", padx=4, pady=2)
        self.var_class = tk.StringVar(value=self.model.klass)
        cb_class = ttk.Combobox(
            self, textvariable=self.var_class, values=CLASSES, state="readonly"
        )
        cb_class.grid(row=4, column=1, sticky="ew", padx=4, pady=2)
        self.var_class.trace_add("write", self._on_class_change)
        # Level selection
        ttk.Label(self, text="Level:").grid(row=5, column=0, sticky="w", padx=4, pady=2)
        self.var_level = tk.IntVar(value=self.model.level)
        spn_level = ttk.Spinbox(self, from_=1, to=20, textvariable=self.var_level, width=5)
        spn_level.grid(row=5, column=1, sticky="w", padx=4, pady=2)
        self.var_level.trace_add("write", self._on_level_change)

        # Background selection
        ttk.Label(self, text="Background:").grid(
            row=6, column=0, sticky="w", padx=4, pady=2
        )
        self.var_bg = tk.StringVar(value=self.model.background)
        cb_bg = ttk.Combobox(
            self,
            textvariable=self.var_bg,
            values=sorted(BACKGROUNDS.keys()),
            state="readonly",
        )
        cb_bg.grid(row=6, column=1, sticky="ew", padx=4, pady=2)
        self.var_bg.trace_add("write", self._on_background_change)

        # Alignment selection
        ttk.Label(self, text="Alignment:").grid(
            row=7, column=0, sticky="w", padx=4, pady=2
        )
        self.var_align = tk.StringVar(value=self.model.alignment)
        cb_align = ttk.Combobox(
            self, textvariable=self.var_align, values=ALIGNMENTS, state="readonly"
        )
        cb_align.grid(row=7, column=1, sticky="ew", padx=4, pady=2)
        self.var_align.trace_add(
            "write", lambda *_: setattr(self.model, "alignment", self.var_align.get())
        )

        # Race detail display
        self.lbl_race_info = ttk.Label(self, justify="left", wraplength=350)
        self.lbl_race_info.grid(row=8, column=0, columnspan=2, sticky="w", padx=4, pady=4)
        self._update_race_display()

    def _on_race_change(self, *_):
        race = self.var_race.get()
        self.model.race = race
        sub_list = SUBRACES.get(race, [])
        if sub_list:
            self.cb_sub.configure(values=sub_list, state="readonly")
        else:
            self.cb_sub.configure(values=[], state="disabled")
            self.var_sub.set("")
            self.model.subrace = None
        self._update_race_display()

    def _on_class_change(self, *_):
        self.model.klass = self.var_class.get()
        for child in self.master.winfo_children():
            if hasattr(child, "refresh_class"):
                child.refresh_class()
            if hasattr(child, "refresh_spells"):
                child.refresh_spells()
            if hasattr(child, "refresh"):
                child.refresh()

    def _on_background_change(self, *_):
        self.model.background = self.var_bg.get()
        for child in self.master.winfo_children():
            if hasattr(child, "refresh_background"):
                child.refresh_background()
            if hasattr(child, "refresh"):
                child.refresh()

    def _on_level_change(self, *_):
        try:
            self.model.level = int(self.var_level.get())
        except tk.TclError:
            self.model.level = 1
        for child in self.master.winfo_children():
            if hasattr(child, "refresh_spells"):
                child.refresh_spells()
            if hasattr(child, "refresh"):
                child.refresh()

    def _on_subrace_change(self, *_):
        self.model.subrace = self.var_sub.get() or None
        self._update_race_display()

    def _update_race_display(self) -> None:
        race = self.model.race
        if not race:
            self.model.race_details = {}
            self.lbl_race_info.configure(text="")
            return
        data = RACES.get(race, {}).copy()
        sub = None
        if self.model.subrace:
            sub = data.get("subraces", {}).get(self.model.subrace, {})
        asi = dict(data.get("asi", {}))
        features = list(data.get("features", []))
        speed = data.get("speed", 30)
        darkvision = data.get("darkvision", 0)
        desc = data.get("description", "")
        if sub:
            desc += f"\n{sub.get('description','')}"
            features.extend(sub.get("features", []))
            if "asi" in sub:
                for k, v in sub["asi"].items():
                    asi[k] = asi.get(k, 0) + v
            speed = sub.get("speed", speed)
            darkvision = sub.get("darkvision", darkvision)
        info = {
            "description": desc,
            "languages": data.get("languages", []),
            "features": features,
            "speed": speed,
            "darkvision": darkvision,
            "asi": asi,
        }
        self.model.race_details = info
        text = (
            f"{desc}\nSpeed {speed} ft, Darkvision {darkvision} ft\n"
            f"Languages: {', '.join(info['languages'])}\n"
            f"Features: {', '.join(features)}"
        )
        self.lbl_race_info.configure(text=text)
        # Notify other screens
        for child in self.master.winfo_children():
            if hasattr(child, "_refresh_any_widgets"):
                child._refresh_any_widgets()
            if hasattr(child, "refresh"):
                child.refresh()


class AbilitiesScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model

        HelpBanner(self, HELP["abilities"]).pack(anchor="w", pady=4)

        # Generation method selection
        self.method_var = tk.StringVar(value=self.model.ability_method)
        method_row = ttk.Frame(self)
        method_row.pack(anchor="w")
        for text, val in [
            ("Manual", "manual"),
            ("Point-Buy", "point"),
            ("Standard Array", "standard"),
        ]:
            ttk.Radiobutton(
                method_row,
                text=text,
                value=val,
                variable=self.method_var,
                command=self._on_method_change,
            ).pack(side="left", padx=4)

        row = ttk.Frame(self)
        row.pack(fill="x", pady=2)
        self.base_vars: Dict[str, tk.IntVar] = {}
        self.final_labels: Dict[str, ttk.Label] = {}
        for ab in ABILITIES:
            var = tk.IntVar(value=self.model.abilities_base[ab])
            var.trace_add("write", lambda *_ , ab=ab, v=var: self._on_ability_change(ab, v))
            self.base_vars[ab] = var
            frame = ttk.Frame(row)
            frame.pack(side="left", padx=4)
            LabeledNumber(frame, ab, var).pack()
            lbl = ttk.Label(frame, text=f"Final: {var.get()}")
            lbl.pack()
            self.final_labels[ab] = lbl

        # Widgets for flexible +1 picks (Half-Elf etc.)
        self.any_frame = ttk.Frame(self)
        self.any_vars = [tk.StringVar(), tk.StringVar()]
        ttk.Label(self.any_frame, text="Choose two abilities for +1:").pack(anchor="w")
        for v in self.any_vars:
            cb = ttk.Combobox(self.any_frame, textvariable=v, values=ABILITIES, state="readonly")
            cb.pack(anchor="w")
            v.trace_add("write", self._on_any_change)
        self.any_frame.pack_forget()

        self._refresh_any_widgets()
        self._recompute()

    def _on_method_change(self) -> None:
        new = self.method_var.get()
        if new == self.model.ability_method:
            return
        if not messagebox.askyesno(
            "Switch Method",
            "Changing ability generation method will reset scores. Continue?",
        ):
            self.method_var.set(self.model.ability_method)
            return
        self.model.ability_method = new
        defaults = {a: (10 if new == "manual" else 8) for a in ABILITIES}
        self.model.abilities_base.update(defaults)
        for ab, var in self.base_vars.items():
            var.set(defaults[ab])
        self._recompute()

    def _refresh_any_widgets(self) -> None:
        asi = self.model.race_details.get("asi", {})
        if "ANY" in asi:
            self.any_frame.pack(anchor="w", pady=4)
        else:
            self.any_frame.pack_forget()
            for v in self.any_vars:
                v.set("")
        self._on_any_change()

    def _on_any_change(self, *_):
        picks = [v.get() for v in self.any_vars if v.get()]
        if len(set(picks)) == 2:
            self.model.asi_any_choices = picks
        else:
            self.model.asi_any_choices = []
        self._recompute()

    def _on_ability_change(self, ab: str, var: tk.IntVar) -> None:
        self.model.abilities_base[ab] = var.get()
        self._recompute()

    def _recompute(self) -> None:
        asi = dict(self.model.race_details.get("asi", {}))
        if "ANY" in asi:
            asi.pop("ANY")
            for ab in self.model.asi_any_choices:
                asi[ab] = asi.get(ab, 0) + 1
        self.model.abilities_final = apply_asi(self.model.abilities_base, asi)
        for ab, lbl in self.final_labels.items():
            lbl.configure(text=f"Final: {self.model.abilities_final.get(ab, 0)}")
        for child in self.master.winfo_children():
            if hasattr(child, "refresh_spells"):
                child.refresh_spells()
            if hasattr(child, "refresh"):
                child.refresh()


class ClassScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        self.info_var = tk.StringVar()
        ttk.Label(self, textvariable=self.info_var).pack(anchor="w", pady=2)
        self.skills_frame = ttk.Frame(self)
        self.skills_frame.pack(anchor="w", pady=4)
        self.skill_vars: Dict[str, tk.BooleanVar] = {}
        self.equip_frame = ttk.Frame(self)
        self.equip_frame.pack(anchor="w", pady=4)
        self.equip_vars: List[tk.StringVar] = []
        self.refresh_class()

    def refresh_class(self) -> None:
        klass = self.model.klass
        saves = CLASS_SAVE_THROWS.get(klass, [])
        hit_die = CLASS_HIT_DIE.get(klass, "1d8")
        self.model.class_saves = saves
        self.model.hit_die = hit_die
        self.info_var.set(f"Saving Throws: {', '.join(saves)} | Hit Die: {hit_die}")
        for child in self.skills_frame.winfo_children():
            child.destroy()
        info = CLASS_SKILL_CHOICES.get(klass, {"choose": 0, "from": []})
        self.choose = info.get("choose", 0)
        ttk.Label(self.skills_frame, text=f"Choose {self.choose} skills:").pack(anchor="w")
        self.skill_vars = {}
        self.model.class_skill_picks = set()
        for sk in info.get("from", []):
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(
                self.skills_frame, text=sk, variable=var, command=self._on_skill_change
            )
            chk.pack(anchor="w")
            self.skill_vars[sk] = var

        for child in self.equip_frame.winfo_children():
            child.destroy()
        self.equip_vars = []
        rows = CLASS_STARTING_EQUIPMENT.get(klass, [])
        self.model.equipment_rows = len(rows)
        self.model.equipment_choices = ["" for _ in rows]
        for options in rows:
            v = tk.StringVar()
            cb = ttk.Combobox(
                self.equip_frame, textvariable=v, values=options, state="readonly"
            )
            cb.pack(anchor="w")
            v.trace_add("write", self._on_equip_change)
            self.equip_vars.append(v)
        self._on_equip_change()

    def _on_skill_change(self) -> None:
        picks = [sk for sk, var in self.skill_vars.items() if var.get()]
        if len(picks) > self.choose:
            # prevent over-selection by unchecking extras
            for sk in picks[self.choose:]:
                self.skill_vars[sk].set(False)
            picks = [sk for sk, var in self.skill_vars.items() if var.get()]
        self.model.class_skill_picks = set(picks)
        for child in self.master.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()

    def _on_equip_change(self, *_):
        self.model.equipment_choices = [v.get() for v in self.equip_vars]
        for child in self.master.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()


class BackgroundScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        self.info_var = tk.StringVar()
        ttk.Label(self, textvariable=self.info_var, justify="left").pack(anchor="w", pady=2)
        self.lang_frame = ttk.Frame(self)
        self.lang_frame.pack(anchor="w", pady=4)
        self.lang_vars: List[tk.StringVar] = []
        self.lang_info_var = tk.StringVar()
        self.refresh_background()

    def refresh_background(self) -> None:
        bg = self.model.background
        data = BACKGROUNDS.get(bg, {})
        text = []
        skills = data.get("skills", [])
        tools = ", ".join(data.get("tools", []))
        equipment = ", ".join(data.get("equipment", []))
        feature = data.get("feature", "")
        text.append(f"Skills: {', '.join(skills)}")
        if tools:
            text.append(f"Tools: {tools}")
        if equipment:
            text.append(f"Equipment: {equipment}")
        if feature:
            text.append(f"Feature: {feature}")
        self.info_var.set("\n".join(text))
        self.model.proficient_skills = set(skills)
        self.model.background_languages = []
        langs = data.get("languages", [])
        for child in self.lang_frame.winfo_children():
            child.destroy()
        self.lang_vars = []
        if isinstance(langs, int):
            self.model.background_languages_needed = langs
            ttk.Label(self.lang_frame, text=f"Choose {langs} languages:").pack(anchor="w")
            ttk.Label(self.lang_frame, textvariable=self.lang_info_var).pack(anchor="w")
            for _ in range(langs):
                v = tk.StringVar()
                cb = ttk.Combobox(
                    self.lang_frame, textvariable=v, values=ALL_LANGUAGES, state="readonly"
                )
                cb.pack(anchor="w")
                v.trace_add("write", self._on_lang_change)
                self.lang_vars.append(v)
            self._on_lang_change()
        else:
            self.model.background_languages_needed = 0
            self.model.background_languages = list(langs)
            if langs:
                ttk.Label(
                    self.lang_frame, text="Languages: " + ", ".join(langs)
                ).pack(anchor="w")

    def _on_lang_change(self, *_):
        seen = set()
        for v in self.lang_vars:
            val = v.get()
            if val in seen:
                v.set("")
            elif val:
                seen.add(val)
        self.model.background_languages = [v.get() for v in self.lang_vars if v.get()]
        remaining = self.model.background_languages_needed - len(self.model.background_languages)
        if remaining > 0:
            self.lang_info_var.set(f"{remaining} remaining")
        else:
            self.lang_info_var.set("All selected")
        for child in self.master.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()


class SpellsScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        self.info_var = tk.StringVar()
        ttk.Label(self, textvariable=self.info_var).pack(anchor="w", pady=2)
        self.spell_frame = ttk.Frame(self)
        self.spell_frame.pack(anchor="w", pady=4)
        self.spell_vars: List[tuple[str, tk.BooleanVar]] = []
        self.refresh_spells()

    def refresh_spells(self) -> None:
        klass = self.model.klass
        for child in self.spell_frame.winfo_children():
            child.destroy()
        self.spell_vars = []
        ability = CLASS_SPELLCASTING_ABILITY.get(klass)
        if not ability:
            self.info_var.set("Selected class has no spellcasting.")
            self.model.spellcasting = {}
            return
        ability_score = self.model.abilities_final.get(ability, self.model.abilities_base.get(ability, 10))
        mod = (ability_score - 10) // 2
        pb = prof_bonus(self.model.level)
        dc = 8 + pb + mod
        attack = pb + mod
        self.model.spellcasting = {
            "ability": ability,
            "dc": dc,
            "attack": attack,
        }
        # Slot reference
        if klass in ("Bard", "Cleric", "Druid", "Sorcerer", "Wizard"):
            slots = FULL_CASTER_SLOTS.get(self.model.level, [])
        elif klass in ("Paladin", "Ranger"):
            eff = HALF_CASTER_LEVEL_MAP.get(self.model.level, self.model.level)
            slots = FULL_CASTER_SLOTS.get(eff, [])
        elif klass == "Warlock":
            slots = WARLOCK_PACT_SLOTS.get(self.model.level, (0, 0))
        else:
            slots = []
        self.model.spellcasting["slots"] = slots
        self.info_var.set(
            f"Casting Ability: {ability} | Save DC {dc} | Attack {attack}"
        )
        spells = SRD_SPELL_LISTS_MIN.get(klass, [])
        for sp in spells:
            var = tk.BooleanVar(value=sp in self.model.chosen_spells)
            chk = ttk.Checkbutton(
                self.spell_frame, text=sp, variable=var, command=self._on_spell_change
            )
            chk.pack(anchor="w")
            self.spell_vars.append((sp, var))
        for child in self.master.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()

    def _on_spell_change(self) -> None:
        self.model.chosen_spells = [sp for sp, var in self.spell_vars if var.get()]
        for child in self.master.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()


class ReviewScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        self.text = tk.Text(self, width=80, height=20)
        self.text.pack(fill="both", expand=True)
        ttk.Button(self, text="Export", command=self._export).pack(pady=4)
        self.refresh()

    def refresh(self) -> None:
        final = self.model.abilities_final or self.model.abilities_base
        pb = prof_bonus(self.model.level)
        profs = set(self.model.proficient_skills) | set(self.model.class_skill_picks)
        skills = compute_skill_bonuses(final, profs, self.model.level)
        init = compute_initiative(final)
        hp = compute_hp_level1(self.model.klass, ability_mod(final.get("CON", 10)))
        speed = self.model.race_details.get("speed", 30)
        dark = self.model.race_details.get("darkvision", 0)
        passive = 10 + skills.get("Perception", 0)
        languages = set(self.model.race_details.get("languages", [])) | set(
            self.model.background_languages
        )
        lines = [
            f"Name: {self.model.name} (Player: {self.model.player})",
            f"Race: {self.model.race} {self.model.subrace or ''}",
            f"Class: {self.model.klass} Level {self.model.level}",
            f"Background: {self.model.background} Alignment: {self.model.alignment}",
            "",
            "Abilities: " + ", ".join(f"{ab} {final[ab]}" for ab in ABILITIES),
            f"Speed {speed} ft, Darkvision {dark} ft",
            f"Saving Throws: {', '.join(self.model.class_saves)} | Hit Die {self.model.hit_die}",
            f"Proficient Skills: {', '.join(sorted(profs))}",
            f"Languages: {', '.join(sorted(languages))}",
            f"Equipment: {', '.join(filter(None, self.model.equipment_choices))}",
            f"HP {hp} | Initiative {init} | Passive Perception {passive}",
        ]
        if self.model.spellcasting:
            sc = self.model.spellcasting
            lines.append(
                f"Spellcasting {sc['ability']} DC {sc['dc']} Attack {sc['attack']}"
            )
            if sc.get("slots"):
                lines.append(f"Slots: {sc['slots']}")
            if self.model.chosen_spells:
                lines.append("Spells: " + ", ".join(self.model.chosen_spells))
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "\n".join(lines))

    def _export(self) -> None:
        errors = []
        if not self.model.name:
            errors.append("Name is required")
        if not self.model.race:
            errors.append("Race is required")
        if not self.model.klass:
            errors.append("Class is required")
        if self.model.background_languages_needed > len(self.model.background_languages):
            errors.append("Select background languages")
        if self.model.ability_method == "point":
            errors.extend(validate_point_buy(self.model.abilities_base))
        elif self.model.ability_method == "standard":
            errors.extend(validate_standard_array(self.model.abilities_base))
        errors.extend(validate_skill_count(self.model.klass, self.model.class_skill_picks))
        if "ANY" in self.model.race_details.get("asi", {}) and len(self.model.asi_any_choices) != 2:
            errors.append("Choose two abilities for racial bonus")
        missing_rows = [
            str(i + 1)
            for i, choice in enumerate(self.model.equipment_choices)
            if not choice
        ]
        if missing_rows:
            errors.append(
                "Pick 1 option in Equipment row(s) " + ", ".join(missing_rows)
            )
        if errors:
            messagebox.showerror("Validation", "\n".join(errors))
            return
        final = self.model.abilities_final or self.model.abilities_base
        profs = set(self.model.proficient_skills) | set(self.model.class_skill_picks)
        skills = compute_skill_bonuses(final, profs, self.model.level)
        init = compute_initiative(final)
        hp = compute_hp_level1(self.model.klass, ability_mod(final.get("CON", 10)))
        speed = self.model.race_details.get("speed", 30)
        dark = self.model.race_details.get("darkvision", 0)
        passive = 10 + skills.get("Perception", 0)
        data = {
            "meta": {
                "name": self.model.name,
                "player": self.model.player,
                "race": self.model.race,
                "subrace": self.model.subrace,
                "class": self.model.klass,
                "level": self.model.level,
                "background": self.model.background,
                "alignment": self.model.alignment,
            },
            "base_abilities": self.model.abilities_base,
            "final_abilities": final,
            "race": self.model.race_details,
            "class": {
                "saves": self.model.class_saves,
                "hit_die": self.model.hit_die,
                "skills": list(self.model.class_skill_picks),
                "equipment": [eq for eq in self.model.equipment_choices if eq],
            },
            "background": {
                "languages": self.model.background_languages,
            },
            "skills": skills,
            "combat": {
                "hp": hp,
                "initiative": init,
                "passive_perception": passive,
                "speed": speed,
                "darkvision": dark,
            },
            "spells": self.model.spellcasting,
            "chosen_spells": self.model.chosen_spells,
        }
        fname = f"{self.model.name.replace(' ', '_')}_character.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Export", f"Character saved to {fname}")

