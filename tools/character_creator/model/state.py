from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional, Set, List, Dict

from ..srd_data import ABILITIES


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
    proficient_skills: Set[str] = field(default_factory=set)
    equipment_choices: List[str] = field(default_factory=list)
    chosen_spells: List[str] = field(default_factory=list)
    spellcasting: Dict[str, object] = field(default_factory=dict)


@dataclass
class Character:
    """Final computed character output."""

    selections: Selections
    abilities: Dict[str, int] = field(default_factory=dict)
    skills: Dict[str, int] = field(default_factory=dict)
    max_hp: int = 0
    initiative: int = 0
    passive_perception: int = 10

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["selections"] = asdict(self.selections)
        return data
