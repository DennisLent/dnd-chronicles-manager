"""Centralised ttk styles."""

from __future__ import annotations

from tkinter import ttk


def setup_styles() -> None:
    style = ttk.Style()
    style.configure("TLabel", padding=2)
    style.configure("TButton", padding=2)
