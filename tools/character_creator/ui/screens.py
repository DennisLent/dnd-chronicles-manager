"""Tkinter screens for the character creator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..config.text import HELP
from ..model.state import Selections
from .widgets import HelpBanner, LabeledNumber


class BasicsScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model

        HelpBanner(self, HELP["abilities"]).pack(fill="x", pady=4)

        self.v_name = tk.StringVar(value="")
        row = ttk.Frame(self)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text="Race:").pack(side="left")
        self.ent_race = ttk.Entry(row, textvariable=tk.StringVar())
        self.ent_race.pack(side="left", padx=4)

        row2 = ttk.Frame(self)
        row2.pack(fill="x", pady=2)
        for ab in self.model.abilities_base:
            var = tk.IntVar(value=self.model.abilities_base[ab])
            LabeledNumber(row2, ab, var).pack(side="left", padx=4)


class ReviewScreen(ttk.Frame):
    def __init__(self, master, model: Selections):
        super().__init__(master)
        self.model = model
        ttk.Label(self, text="Review character and export.").pack(anchor="w")
