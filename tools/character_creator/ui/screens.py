"""Tkinter screens for the character creator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..config.text import HELP
from ..model.state import Selections
from ..srd_data import (
    ABILITIES,
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
        self.var_sub.trace_add(
            "write", lambda *_: setattr(self.model, "subrace", self.var_sub.get() or None)
        )

        # Class selection
        ttk.Label(self, text="Class:").grid(row=4, column=0, sticky="w", padx=4, pady=2)
        self.var_class = tk.StringVar(value=self.model.klass)
        cb_class = ttk.Combobox(
            self, textvariable=self.var_class, values=CLASSES, state="readonly"
        )
        cb_class.grid(row=4, column=1, sticky="ew", padx=4, pady=2)
        self.var_class.trace_add(
            "write", lambda *_: setattr(self.model, "klass", self.var_class.get())
        )

        # Background selection
        ttk.Label(self, text="Background:").grid(
            row=5, column=0, sticky="w", padx=4, pady=2
        )
        self.var_bg = tk.StringVar(value=self.model.background)
        cb_bg = ttk.Combobox(
            self,
            textvariable=self.var_bg,
            values=sorted(BACKGROUNDS.keys()),
            state="readonly",
        )
        cb_bg.grid(row=5, column=1, sticky="ew", padx=4, pady=2)
        self.var_bg.trace_add(
            "write", lambda *_: setattr(self.model, "background", self.var_bg.get())
        )

        # Alignment selection
        ttk.Label(self, text="Alignment:").grid(
            row=6, column=0, sticky="w", padx=4, pady=2
        )
        self.var_align = tk.StringVar(value=self.model.alignment)
        cb_align = ttk.Combobox(
            self, textvariable=self.var_align, values=ALIGNMENTS, state="readonly"
        )
        cb_align.grid(row=6, column=1, sticky="ew", padx=4, pady=2)
        self.var_align.trace_add(
            "write", lambda *_: setattr(self.model, "alignment", self.var_align.get())
        )

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


class AbilitiesScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model

        HelpBanner(self, HELP["abilities"]).pack(anchor="w", pady=4)

        row = ttk.Frame(self)
        row.pack(fill="x", pady=2)
        for ab in ABILITIES:
            var = tk.IntVar(value=self.model.abilities_base[ab])
            var.trace_add(
                "write", lambda *_ , ab=ab, v=var: self._on_ability_change(ab, v)
            )
            LabeledNumber(row, ab, var).pack(side="left", padx=4)

    def _on_ability_change(self, ab: str, var: tk.IntVar) -> None:
        self.model.abilities_base[ab] = var.get()


class ReviewScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        ttk.Label(self, text="Review character and export.").pack(anchor="w")

