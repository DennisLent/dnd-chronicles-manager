"""Reusable Tkinter widgets."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.interior = ttk.Frame(canvas)
        self.interior.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.interior, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")


class LabeledNumber(ttk.Frame):
    def __init__(self, master, text: str, var: tk.IntVar, **kwargs):
        super().__init__(master, **kwargs)
        ttk.Label(self, text=text).pack(side="left")
        self.spin = tk.Spinbox(self, from_=-10, to=30, textvariable=var, width=5)
        self.spin.pack(side="left", padx=4)


class HelpBanner(ttk.Frame):
    def __init__(self, master, text: str, **kwargs):
        super().__init__(master, **kwargs)
        lbl = ttk.Label(self, text=text, foreground="blue")
        lbl.pack(anchor="w")
