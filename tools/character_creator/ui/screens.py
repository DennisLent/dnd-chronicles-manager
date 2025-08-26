"""Tkinter screens for the character creator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..config.text import HELP
from ..model.state import Selections
from ..srd_data import (
    ALIGNMENTS,
    BACKGROUNDS,
    CLASSES,
    RACES,
    SUBRACES,
)
from .widgets import HelpBanner, LabeledNumber


class BasicsScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model

        HelpBanner(self, HELP["abilities"]).pack(fill="x", pady=4)

        # --- Basic information inputs ---
        row = ttk.Frame(self)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text="Name:").pack(side="left")
        self.var_name = tk.StringVar(value=self.model.name)
        ent_name = ttk.Entry(row, textvariable=self.var_name)
        ent_name.pack(side="left", padx=4)
        self.var_name.trace_add("write", lambda *_: setattr(self.model, "name", self.var_name.get()))

        row_player = ttk.Frame(self)
        row_player.pack(fill="x", pady=2)
        ttk.Label(row_player, text="Player:").pack(side="left")
        self.var_player = tk.StringVar(value=self.model.player)
        ent_player = ttk.Entry(row_player, textvariable=self.var_player)
        ent_player.pack(side="left", padx=4)
        self.var_player.trace_add("write", lambda *_: setattr(self.model, "player", self.var_player.get()))

        row_race = ttk.Frame(self)
        row_race.pack(fill="x", pady=2)
        ttk.Label(row_race, text="Race:").pack(side="left")
        self.var_race = tk.StringVar(value=self.model.race)
        self.cb_race = ttk.Combobox(
            row_race,
            textvariable=self.var_race,
            values=sorted(RACES.keys()),
            state="readonly",
        )
        self.cb_race.pack(side="left", padx=4)
        self.var_race.trace_add("write", self._on_race_change)

        row_sub = ttk.Frame(self)
        row_sub.pack(fill="x", pady=2)
        ttk.Label(row_sub, text="Subrace:").pack(side="left")
        self.var_sub = tk.StringVar(value=self.model.subrace or "")
        self.cb_sub = ttk.Combobox(row_sub, textvariable=self.var_sub, state="disabled")
        self.cb_sub.pack(side="left", padx=4)
        self.var_sub.trace_add(
            "write", lambda *_: setattr(self.model, "subrace", self.var_sub.get() or None)
        )

        row_class = ttk.Frame(self)
        row_class.pack(fill="x", pady=2)
        ttk.Label(row_class, text="Class:").pack(side="left")
        self.var_class = tk.StringVar(value=self.model.klass)
        cb_class = ttk.Combobox(row_class, textvariable=self.var_class, values=CLASSES, state="readonly")
        cb_class.pack(side="left", padx=4)
        self.var_class.trace_add("write", lambda *_: setattr(self.model, "klass", self.var_class.get()))

        row_level = ttk.Frame(self)
        row_level.pack(fill="x", pady=2)
        ttk.Label(row_level, text="Level:").pack(side="left")
        self.var_level = tk.IntVar(value=self.model.level)
        spn_level = tk.Spinbox(row_level, from_=1, to=20, textvariable=self.var_level, width=5)
        spn_level.pack(side="left", padx=4)
        self.var_level.trace_add("write", lambda *_: setattr(self.model, "level", self.var_level.get()))

        row_bg = ttk.Frame(self)
        row_bg.pack(fill="x", pady=2)
        ttk.Label(row_bg, text="Background:").pack(side="left")
        self.var_bg = tk.StringVar(value=self.model.background)
        cb_bg = ttk.Combobox(
            row_bg,
            textvariable=self.var_bg,
            values=sorted(BACKGROUNDS.keys()),
            state="readonly",
        )
        cb_bg.pack(side="left", padx=4)
        self.var_bg.trace_add("write", lambda *_: setattr(self.model, "background", self.var_bg.get()))

        row_align = ttk.Frame(self)
        row_align.pack(fill="x", pady=2)
        ttk.Label(row_align, text="Alignment:").pack(side="left")
        self.var_align = tk.StringVar(value=self.model.alignment)
        cb_align = ttk.Combobox(row_align, textvariable=self.var_align, values=ALIGNMENTS, state="readonly")
        cb_align.pack(side="left", padx=4)
        self.var_align.trace_add("write", lambda *_: setattr(self.model, "alignment", self.var_align.get()))

        # --- Ability score inputs ---
        row2 = ttk.Frame(self)
        row2.pack(fill="x", pady=2)
        for ab in self.model.abilities_base:
            var = tk.IntVar(value=self.model.abilities_base[ab])
            var.trace_add("write", lambda *_ , ab=ab, v=var: self._on_ability_change(ab, v))
            LabeledNumber(row2, ab, var).pack(side="left", padx=4)

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

    def _on_ability_change(self, ab: str, var: tk.IntVar) -> None:
        self.model.abilities_base[ab] = var.get()


class ReviewScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        ttk.Label(self, text="Review character and export.").pack(anchor="w")

