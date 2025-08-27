"""Thin Tkinter entry point for the character creator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .model.state import Selections
from .io.serialize import load_character
from .ui.screens import (
    AbilitiesScreen,
    BasicsScreen,
    ClassScreen,
    BackgroundScreen,
    SpellsScreen,
    ReviewScreen,
)
from .ui.styles import setup_styles


def main() -> None:
    root = tk.Tk()
    root.title("DnD 5e Character Creator")
    root.geometry("800x600")
    setup_styles()

    model = Selections.load_draft() or Selections()

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    basics = BasicsScreen(nb, model)
    abilities = AbilitiesScreen(nb, model)
    cls = ClassScreen(nb, model)
    bg = BackgroundScreen(nb, model)
    spells = SpellsScreen(nb, model)
    review = ReviewScreen(nb, model)
    nb.add(basics, text="Basics")
    nb.add(abilities, text="Abilities")
    nb.add(cls, text="Class")
    nb.add(bg, text="Background")
    nb.add(spells, text="Spells")
    nb.add(review, text="Review")

    if Selections.load_draft() is not None:
        if not messagebox.askyesno("Resume", "Resume draft character?"):
            model = Selections()
            basics.model = abilities.model = cls.model = bg.model = spells.model = review.model = model
            Selections.clear_draft()
            for scr in (basics, abilities, cls, bg, spells, review):
                if hasattr(scr, "refresh"):
                    scr.refresh()

    def refresh_all() -> None:
        for scr in (basics, abilities, cls, bg, spells, review):
            if hasattr(scr, "refresh"):
                scr.refresh()

    def open_character() -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        char = load_character(path)
        nonlocal model
        model = char.selections
        basics.model = abilities.model = cls.model = bg.model = spells.model = review.model = model
        refresh_all()

    def reset_all() -> None:
        nonlocal model
        model = Selections()
        basics.model = abilities.model = cls.model = bg.model = spells.model = review.model = model
        Selections.clear_draft()
        refresh_all()

    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open…", command=open_character)
    file_menu.add_command(label="Reset", command=reset_all)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    main()
