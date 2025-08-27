from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
from typing import Any, Optional, List, Dict
import tkinter as tk

from ..srd_data import ABILITIES

_DRAFT_FILE = Path(__file__).resolve().parent / "draft.json"


@dataclass
class Selections:
    """User choices captured during character creation."""

    name: str = ""
    player: str = ""
    race: str = ""
    subrace: Optional[str] = None
    klass: str = ""
    level: int = 1
    background: str = ""
    alignment: str = "True Neutral"
    ability_method: str = "manual"
    abilities_base: Dict[str, int] = field(
        default_factory=lambda: {a: 10 for a in ABILITIES}
    )
    # Cached race info (merged race + subrace block)
    race_details: Dict[str, object] = field(default_factory=dict)
    # Final ability scores after racial ASIs
    abilities_final: Dict[str, int] = field(default_factory=dict)
    # For races like Half-Elf that grant flexible +1 bonuses
    asi_any_choices: List[str] = field(default_factory=list)
    # Class derived data
    class_skill_picks: List[str] = field(default_factory=list)
    class_saves: List[str] = field(default_factory=list)
    hit_die: str = ""
    # Background language selections (if background grants choices)
    background_languages: List[str] = field(default_factory=list)
    background_languages_needed: int = 0
    background_details: Dict[str, object] = field(default_factory=dict)
    proficient_skills: List[str] = field(default_factory=list)
    equipment_choices: List[str] = field(default_factory=list)
    equipment_rows: int = 0
    chosen_spells: List[str] = field(default_factory=list)
    spellcasting: Dict[str, object] = field(default_factory=dict)

    _root: Optional[tk.Misc] = field(default=None, repr=False, compare=False)
    _save_after: Optional[str] = field(default=None, repr=False, compare=False)

    def attach_root(self, root: tk.Misc) -> None:
        """Attach Tk root to enable debounced saving."""
        self._root = root

    def _to_jsonable(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._to_jsonable(v) for k, v in obj.items()}
        if isinstance(obj, set):
            return sorted(self._to_jsonable(v) for v in obj)
        if isinstance(obj, list):
            return [self._to_jsonable(v) for v in obj]
        return obj

    def save_draft(self) -> None:
        """Persist current selections to a temporary draft file with debounce."""
        if self._root is not None:
            if self._save_after:
                self._root.after_cancel(self._save_after)
            self._save_after = self._root.after(250, self._write_draft)
        else:
            self._write_draft()

    def _write_draft(self) -> None:
        try:
            data = self._to_jsonable(asdict(self))
            with open(_DRAFT_FILE, "w", encoding="utf-8") as fh:
                json.dump(data, fh, sort_keys=True, indent=2)
        except Exception as exc:  # pragma: no cover - debug aid
            print(f"draft save failed: {exc}")
        finally:
            if self._root is not None:
                self._save_after = None

    @staticmethod
    def load_draft() -> Optional["Selections"]:
        if not _DRAFT_FILE.exists():
            return None
        with open(_DRAFT_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return Selections(**data)

    @staticmethod
    def clear_draft() -> None:
        if _DRAFT_FILE.exists():
            _DRAFT_FILE.unlink()


@dataclass
class Character:
    """Final computed character output."""

    selections: Selections
    data: Dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        out = dict(self.data)
        out["selections"] = asdict(self.selections)
        return out
