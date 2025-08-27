from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
from typing import Optional, Set, List, Dict

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
    class_skill_picks: Set[str] = field(default_factory=set)
    class_saves: List[str] = field(default_factory=list)
    hit_die: str = ""
    # Background language selections (if background grants choices)
    background_languages: List[str] = field(default_factory=list)
    background_languages_needed: int = 0
    background_details: Dict[str, object] = field(default_factory=dict)
    proficient_skills: Set[str] = field(default_factory=set)
    equipment_choices: List[str] = field(default_factory=list)
    equipment_rows: int = 0
    chosen_spells: List[str] = field(default_factory=list)
    spellcasting: Dict[str, object] = field(default_factory=dict)

    def save_draft(self) -> None:
        """Persist current selections to a temporary draft file."""
        with open(_DRAFT_FILE, "w", encoding="utf-8") as fh:
            json.dump(asdict(self), fh, sort_keys=True, indent=2)

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
