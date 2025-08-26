"""Thin Tkinter entry point for the character creator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .model.state import Selections
from .ui.screens import BasicsScreen, ReviewScreen
from .ui.styles import setup_styles


def main() -> None:
    root = tk.Tk()
    root.title("DnD 5e Character Creator")
    root.geometry("800x600")
    setup_styles()

    model = Selections()

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    nb.add(BasicsScreen(nb, model), text="Basics")
    nb.add(ReviewScreen(nb, model), text="Review")

    root.mainloop()


if __name__ == "__main__":
    main()
