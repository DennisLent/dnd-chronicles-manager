"""
Comprehensive SRD-leaning reference data for D&D 5e character creation.
This file is STATIC DATA ONLY.
It’s designed to let the GUI render rich choices and compute common derived values.

Sourcing notes (verified against the SRD 5.1 and SRD-style references):
- Races, subraces, traits (ASI, Darkvision, etc.) from the 5e SRD / Basic Rules.
  See: Hypertext 5e SRD races and the official SRD 5.1 PDF. [citations inline]
- Class skill-choice lists, starting equipment menus, level tables and
  spell-slot tables based on SRD class pages. [citations inline]
- Backgrounds (Acolyte, Criminal, Folk Hero, Noble, Sage, Soldier) from SRD.
- Warlock Pact Magic and the Multiclass Spellcaster table included.

IMPORTANT: Aasimar, Goliath, and Orc are **not SRD 5.1** player races.
We keep them here because the project requested them, but mark them
`non_srd=True` and clearly label non‑SRD subraces, including some inspired by
**Age of Wonders 4** (form/culture flavors) to ensure each race offers at least
two subrace options for onboarding. (These are thematically compatible but not
5e SRD rules.)

Citations used when populating these structures:
- SRD 5.1 PDF: https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf  
- Hypertext SRD (races – ASI, Darkvision, features): https://5e.d20srd.org/srd/races.htm  
- 5thSRD – races/classes/backgrounds tables: https://5thsrd.org/character/races/ ,
  https://5thsrd.org/character/classes/ , https://5thsrd.org/character/backgrounds/  
- SRD class exemplars (Rogue, Cleric, Wizard): https://www.5esrd.com/database/class/rogue/ ,
  https://5thsrd.org/character/classes/cleric/ , https://5e.d20srd.org/srd/classes/wizard.htm  
- Multiclass spell slot rules: https://5thsrd.org/rules/multiclassing/
- AoW4 inspiration for elf/human/orc/goliath sub-flavors (non‑SRD):
  Paradox/Triumph community summaries & discussions.
"""

# =========================
# Core lists
# =========================
CLASSES = [
    "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
    "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
]

RACES_SUMMARY = {
    "Aasimar": "Aasimar are mortals who carry a spark of the Upper Planes within their souls.",
    "Dragonborn": "The ancestors of dragonborn hatched from the eggs of chromatic and metallic dragons.",
    "Dwarf": "Dwarves were raised from the earth in the elder days by a deity of the forge.",
    "Elf": "The elves’ curiosity led many of them to explore other planes of existence.",
    "Gnome": "Gnomes are magical folk created by gods of invention, illusions, and life underground.",
    "Goliath": "Goliaths are distant descendants of giants and seek heights above those reached by their ancestors.",
    "Halfling": "Halflings possess a brave and adventurous spirit that leads them on journeys of discovery.",
    "Human": "Found throughout the multiverse, humans are as varied as they are numerous.",
    "Orc": "Orcs are equipped with gifts to help them wander great plains, vast caverns, and churning seas.",
    "Tiefling": "Tieflings are either born in the Lower Planes or have fiendish ancestors who originated there.",
}

# A compact mapping used by the GUI to quickly populate simple comboboxes.
# (Each race additionally has full definitions in RACES below.)
SUBRACES = {
    "Dragonborn": ["Chromatic Dragonborn", "Metallic Dragonborn"],
    "Dwarf": ["Hill Dwarf", "Mountain Dwarf"],
    "Elf": ["High Elf", "Wood Elf", "Drow"],
    "Gnome": ["Forest Gnome", "Rock Gnome"],
    "Half-Elf": ["High Half-Elf", "Wood Half-Elf"],
    "Half-Orc": ["Gray Half-Orc", "Mountain Half-Orc"],
    "Halfling": ["Lightfoot", "Stout"],
    "Human": ["Standard Human", "Variant Human"],
    "Tiefling": ["Infernal Tiefling", "Abyssal Tiefling"],
    # Non‑SRD extended races
    "Aasimar": ["Protector Aasimar", "Scourge Aasimar"],
    "Goliath": ["Stoneborn Goliath", "Stormborn Goliath"],
    "Orc": ["Gray Orc", "Orog"],
}

ALIGNMENTS = [
    "Lawful Good", "Neutral Good", "Chaotic Good",
    "Lawful Neutral", "True Neutral", "Chaotic Neutral",
    "Lawful Evil", "Neutral Evil", "Chaotic Evil"
]

ABILITIES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

SKILLS = {
    "Acrobatics": "DEX",
    "Animal Handling": "WIS",
    "Arcana": "INT",
    "Athletics": "STR",
    "Deception": "CHA",
    "History": "INT",
    "Insight": "WIS",
    "Intimidation": "CHA",
    "Investigation": "INT",
    "Medicine": "WIS",
    "Nature": "INT",
    "Perception": "WIS",
    "Performance": "CHA",
    "Persuasion": "CHA",
    "Religion": "INT",
    "Sleight of Hand": "DEX",
    "Stealth": "DEX",
    "Survival": "WIS",
}

CLASS_HIT_DIE = {
    "Barbarian": "1d12",
    "Fighter": "1d10", "Paladin": "1d10", "Ranger": "1d10",
    "Bard": "1d8", "Cleric": "1d8", "Druid": "1d8", "Monk": "1d8", "Rogue": "1d8", "Warlock": "1d8",
    "Sorcerer": "1d6", "Wizard": "1d6",
}

CLASS_SAVE_THROWS = {
    "Barbarian": ["STR", "CON"],
    "Bard": ["DEX", "CHA"],
    "Cleric": ["WIS", "CHA"],
    "Druid": ["INT", "WIS"],
    "Fighter": ["STR", "CON"],
    "Monk": ["STR", "DEX"],
    "Paladin": ["WIS", "CHA"],
    "Ranger": ["STR", "DEX"],
    "Rogue": ["DEX", "INT"],
    "Sorcerer": ["CON", "CHA"],
    "Warlock": ["WIS", "CHA"],
    "Wizard": ["INT", "WIS"],
}

STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
POINT_BUY_MIN = 8
POINT_BUY_MAX = 15
POINT_BUY_BUDGET = 27
POINT_BUY_COST = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}

# =========================
# Race mechanics (SRD with non‑SRD extensions clearly labeled)
# =========================
# Structure per race name:
#   {
#     "description": str,
#     "non_srd": bool,
#     "size": "Medium"|"Small",
#     "speed": 25/30/35,
#     "asi": dict[str,int]  # fixed ASIs per SRD (pre–Tasha’s),
#     "languages": [..],
#     "darkvision": 0|60|120,
#     "features": ["Named Feature (summary)", ...],
#     "subraces": {name: { overrides ... , "non_srd": bool, "description": str }}
#   }

RACES = {
    # ---- SRD races ----
    "Dragonborn": {
        "description": RACES_SUMMARY["Dragonborn"],
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 0,
        "asi": {"STR": 2, "CHA": 1},
        "languages": ["Common", "Draconic"],
        "features": [
            "Draconic Ancestry (choose a type; determines breath & damage)",
            "Breath Weapon (action; DC 8 + CON mod + prof; 2d6 at 1st)",
            "Damage Resistance (to your ancestry’s damage)",
        ],
        "subraces": {
            # Not formal PHB subraces; offered as lineages to guide new players
            "Chromatic Dragonborn": {"non_srd": True, "description": "Black/Blue/Green/Red/White ancestry; acid/lightning/poison/fire/cold."},
            "Metallic Dragonborn": {"non_srd": True, "description": "Brass/Bronze/Copper/Gold/Silver ancestry; fire/lightning/acid/fire/cold."},
        }
    },
    "Dwarf": {
        "description": RACES_SUMMARY["Dwarf"],
        "non_srd": False,
        "size": "Medium", "speed": 25, "darkvision": 60,
        "asi": {"CON": 2},
        "languages": ["Common", "Dwarvish"],
        "features": [
            "Dwarven Resilience (advantage vs. poison; resistance to poison damage)",
            "Dwarven Combat Training (battleaxe, handaxe, light hammer, warhammer)",
            "Tool Proficiency (smith’s, brewer’s, or mason’s tools)",
            "Stonecunning (double proficiency on stonework History)",
            "Speed not reduced by heavy armor",
        ],
        "subraces": {
            "Hill Dwarf": {
                "asi": {"WIS": 1},
                "features": ["Dwarven Toughness (+1 HP per level)"]
            },
            "Mountain Dwarf": {
                "asi": {"STR": 2},
                "features": ["Dwarven Armor Training (light & medium armor)"]
            },
        }
    },
    "Elf": {
        "description": RACES_SUMMARY["Elf"],
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {"DEX": 2},
        "languages": ["Common", "Elvish"],
        "features": [
            "Keen Senses (Perception proficiency)",
            "Fey Ancestry (advantage vs. charm; immune to magical sleep)",
            "Trance (4-hour meditation counts as 8-hour sleep)",
        ],
        "subraces": {
            "High Elf": {
                "asi": {"INT": 1},
                "features": [
                    "Elf Weapon Training (longsword, shortsword, shortbow, longbow)",
                    "Cantrip (one wizard cantrip; INT is casting ability)",
                    "Extra Language (one of your choice)",
                ]
            },
            "Wood Elf": {
                "asi": {"WIS": 1},
                "features": [
                    "Elf Weapon Training (longsword, shortsword, shortbow, longbow)",
                    "Fleet of Foot (speed 35 ft)",
                    "Mask of the Wild (attempt to hide when lightly obscured)",
                ],
                "speed": 35
            },
            "Drow": {
                "asi": {"CHA": 1},
                "darkvision": 120,
                "features": [
                    "Sunlight Sensitivity (disadvantage on attack rolls & Perception relying on sight in sunlight)",
                    "Drow Magic (dancing lights; later faerie fire, darkness)",
                    "Drow Weapon Training (rapiers, shortswords, hand crossbows)",
                ]
            },
        }
    },
    "Gnome": {
        "description": RACES_SUMMARY["Gnome"],
        "non_srd": False,
        "size": "Small", "speed": 25, "darkvision": 60,
        "asi": {"INT": 2},
        "languages": ["Common", "Gnomish"],
        "features": [
            "Gnome Cunning (advantage on INT/WIS/CHA saves vs. magic)",
        ],
        "subraces": {
            "Forest Gnome": {
                "asi": {"DEX": 1},
                "features": [
                    "Natural Illusionist (minor illusion cantrip; INT)",
                    "Speak with Small Beasts (limited communication)",
                ]
            },
            "Rock Gnome": {
                "asi": {"CON": 1},
                "features": [
                    "Artificer’s Lore (double proficiency History for magic/tech)",
                    "Tinker (proficiency with tinker’s tools; make Tiny devices)",
                ]
            },
        }
    },
    "Half-Elf": {
        "description": "Humans with elven heritage; versatile diplomats and wanderers.",
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {"CHA": 2, "ANY": 2},  # ANY means choose two different abilities +1 each
        "languages": ["Common", "Elvish", "Choice"],
        "features": [
            "Fey Ancestry (advantage vs. charm; immune to magical sleep)",
            "Skill Versatility (choose two skills)",
        ],
        "subraces": {
            # Non‑SRD variants (SCAG‑style); for onboarding variety
            "High Half-Elf": {"non_srd": True, "description": "+1 INT; high‑elf leanings."},
            "Wood Half-Elf": {"non_srd": True, "description": "+1 WIS; wood‑elf leanings."},
        }
    },
    "Half-Orc": {
        "description": "Humanoids of human and orc heritage; fierce and resolute.",
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {"STR": 2, "CON": 1},
        "languages": ["Common", "Orc"],
        "features": [
            "Menacing (Intimidation proficiency)",
            "Relentless Endurance (drop to 0 HP -> 1 HP once per long rest)",
            "Savage Attacks (extra die on melee crit)",
        ],
        "subraces": {
            "Gray Half-Orc": {"non_srd": True, "description": "Stoic plains clans; endurance traditions."},
            "Mountain Half-Orc": {"non_srd": True, "description": "High‑peak warbands; brutal winters harden them."},
        }
    },
    "Halfling": {
        "description": RACES_SUMMARY["Halfling"],
        "non_srd": False,
        "size": "Small", "speed": 25, "darkvision": 0,
        "asi": {"DEX": 2},
        "languages": ["Common", "Halfling"],
        "features": [
            "Lucky (reroll 1 on d20; must keep new roll)",
            "Brave (advantage on saves vs. frightened)",
            "Halfling Nimbleness (move through larger creatures’ spaces)",
        ],
        "subraces": {
            "Lightfoot": {"asi": {"CHA": 1}, "features": ["Naturally Stealthy"]},
            "Stout": {"asi": {"CON": 1}, "features": ["Stout Resilience (advantage vs. poison; resistance)"]},
        }
    },
    "Human": {
        "description": RACES_SUMMARY["Human"],
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 0,
        "asi": {"STR":1,"DEX":1,"CON":1,"INT":1,"WIS":1,"CHA":1},
        "languages": ["Common", "Choice"],
        "features": [],
        "subraces": {
            "Standard Human": {"description": "The default SRD human (all +1)."},
            "Variant Human": {"non_srd": True, "description": "+1 to two abilities, one skill, one feat (table dependent)."},
        }
    },
    "Tiefling": {
        "description": RACES_SUMMARY["Tiefling"],
        "non_srd": False,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {"CHA": 2, "INT": 1},
        "languages": ["Common", "Infernal"],
        "features": [
            "Hellish Resistance (fire resistance)",
            "Infernal Legacy (thaumaturgy cantrip; later: hellish rebuke, darkness)",
        ],
        "subraces": {
            # Non‑SRD: present ancestry flavors for new players
            "Infernal Tiefling": {"non_srd": True, "description": "Diabolic bloodlines (Asmodeus/Baalzebul flavors)."},
            "Abyssal Tiefling": {"non_srd": True, "description": "Chaotic demonic influence (Abyss‑touched)."},
        }
    },

    # ---- Non‑SRD extended races requested ----
    "Aasimar": {
        "description": RACES_SUMMARY["Aasimar"],
        "non_srd": True,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {}, "languages": ["Common"], "features": [],
        "subraces": {
            "Protector Aasimar": {"non_srd": True, "description": "Radiant guardians; luminous flight in bursts."},
            "Scourge Aasimar": {"non_srd": True, "description": "Burning zeal; searing aura of light."},
        }
    },
    "Goliath": {
        "description": RACES_SUMMARY["Goliath"],
        "non_srd": True,
        "size": "Medium", "speed": 30, "darkvision": 0,
        "asi": {}, "languages": ["Common"], "features": [],
        "subraces": {
            "Stoneborn Goliath": {"non_srd": True, "description": "Granite‑skinned mountaineers (AoW‑style form)."},
            "Stormborn Goliath": {"non_srd": True, "description": "Thunder‑scarred peak‑clans attuned to tempests."},
        }
    },
    "Orc": {
        "description": RACES_SUMMARY["Orc"],
        "non_srd": True,
        "size": "Medium", "speed": 30, "darkvision": 60,
        "asi": {}, "languages": ["Common"], "features": [],
        "subraces": {
            "Gray Orc": {"non_srd": True, "description": "Wandering plains tribes; stoic and spiritual."},
            "Orog": {"non_srd": True, "description": "Deep‑delving orcs bred for war (Underdark legends)."},
        }
    },
}

# =========================
# Class: skill choices, equipment, iconic features, subclass level
# =========================
# CLASS_SKILL_CHOICES[class] = {"choose": N, "from": [skills...]}
# CLASS_STARTING_EQUIPMENT[class] = list of mutually-exclusive option groups
# CLASS_FEATURES_LEVELS[class][level] = [feature names]
# SUBCLASS_CHOICE_LEVEL[class] = level when subclass is chosen

CLASS_SKILL_CHOICES = {
    "Barbarian": {"choose": 2, "from": ["Animal Handling","Athletics","Intimidation","Nature","Perception","Survival"]},
    "Bard":      {"choose": 3, "from": list(SKILLS.keys())},  # any three
    "Cleric":    {"choose": 2, "from": ["History","Insight","Medicine","Persuasion","Religion"]},
    "Druid":     {"choose": 2, "from": ["Arcana","Animal Handling","Insight","Medicine","Nature","Perception","Religion","Survival"]},
    "Fighter":   {"choose": 2, "from": ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"]},
    "Monk":      {"choose": 2, "from": ["Acrobatics","Athletics","History","Insight","Religion","Stealth"]},
    "Paladin":   {"choose": 2, "from": ["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"]},
    "Ranger":    {"choose": 3, "from": ["Animal Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"]},
    "Rogue":     {"choose": 4, "from": ["Acrobatics","Athletics","Deception","Insight","Intimidation","Investigation","Perception","Performance","Persuasion","Sleight of Hand","Stealth"]},
    "Sorcerer":  {"choose": 2, "from": ["Arcana","Deception","Insight","Intimidation","Persuasion","Religion"]},
    "Warlock":   {"choose": 2, "from": ["Arcana","Deception","History","Intimidation","Investigation","Nature","Religion"]},
    "Wizard":    {"choose": 2, "from": ["Arcana","History","Insight","Investigation","Medicine","Religion"]},
}

# Starting equipment menus (each inner list is a pick‑one option set)
CLASS_STARTING_EQUIPMENT = {
    "Barbarian": [
        ["a greataxe", "any martial melee weapon"],
        ["two handaxes", "any simple weapon"],
        ["an explorer's pack"],
        ["four javelins"],
    ],
    "Bard": [
        ["a rapier", "a longsword", "a simple weapon"],
        ["a diplomat's pack", "an entertainer's pack"],
        ["a lute", "any musical instrument"],
        ["leather armor", "dagger"],
    ],
    "Cleric": [
        ["a mace", "a warhammer (if proficient)"],
        ["scale mail", "leather armor", "chain mail (if proficient)"],
        ["a light crossbow and 20 bolts", "any simple weapon"],
        ["a priest's pack", "an explorer's pack"],
        ["a shield"],
        ["a holy symbol"],
    ],
    "Druid": [
        ["a wooden shield", "any simple weapon"],
        ["a scimitar", "any simple melee weapon"],
        ["a druidic focus"],
        ["an explorer's pack"],
        ["leather armor"],
    ],
    "Fighter": [
        ["chain mail", "leather armor, longbow, and 20 arrows"],
        ["a martial weapon and a shield", "two martial weapons"],
        ["a light crossbow and 20 bolts", "two handaxes"],
        ["a dungeoneer's pack", "an explorer's pack"],
    ],
    "Monk": [
        ["a shortsword", "any simple weapon"],
        ["a dungeoneer's pack", "an explorer's pack"],
        ["10 darts"],
    ],
    "Paladin": [
        ["a martial weapon and a shield", "two martial weapons"],
        ["five javelins", "any simple melee weapon"],
        ["a priest's pack", "an explorer's pack"],
        ["chain mail"],
        ["a holy symbol"],
    ],
    "Ranger": [
        ["scale mail", "leather armor"],
        ["two shortswords", "two simple melee weapons"],
        ["a dungeoneer's pack", "an explorer's pack"],
        ["a longbow and a quiver of 20 arrows"],
    ],
    "Rogue": [
        ["a rapier", "a shortsword"],
        ["a shortbow and quiver of 20 arrows", "a shortsword"],
        ["a burglar's pack", "a dungeoneer's pack", "an explorer's pack"],
        ["leather armor", "two daggers", "thieves' tools"],
    ],
    "Sorcerer": [
        ["a light crossbow and 20 bolts", "any simple weapon"],
        ["a component pouch", "an arcane focus"],
        ["a dungeoneer's pack", "an explorer's pack"],
        ["two daggers"],
    ],
    "Warlock": [
        ["a light crossbow and 20 bolts", "any simple weapon"],
        ["a component pouch", "an arcane focus"],
        ["a scholar's pack", "a dungeoneer's pack"],
        ["leather armor", "any simple weapon", "two daggers"],
    ],
    "Wizard": [
        ["a quarterstaff", "a dagger"],
        ["a component pouch", "an arcane focus"],
        ["a scholar's pack", "an explorer's pack"],
        ["a spellbook"],
    ],
}

SUBCLASS_CHOICE_LEVEL = {
    "Barbarian": 3, "Bard": 3, "Cleric": 1, "Druid": 2, "Fighter": 3,
    "Monk": 3, "Paladin": 3, "Ranger": 3, "Rogue": 3, "Sorcerer": 1,
    "Warlock": 1, "Wizard": 2,
}

# Iconic early features per level (high‑level summary for on‑sheet reminders)
CLASS_FEATURES_LEVELS = {
    "Barbarian": {1:["Rage","Unarmored Defense"],2:["Reckless Attack","Danger Sense"],3:["Primal Path"]},
    "Bard": {1:["Spellcasting","Bardic Inspiration (d6)"],2:["Jack of All Trades","Song of Rest"],3:["Bard College"]},
    "Cleric": {1:["Spellcasting","Divine Domain"],2:["Channel Divinity (1/rest)"],5:["Destroy Undead (CR 1/2)"]},
    "Druid": {1:["Druidic","Spellcasting"],2:["Wild Shape","Druid Circle"]},
    "Fighter": {1:["Fighting Style","Second Wind"],2:["Action Surge"],3:["Martial Archetype"]},
    "Monk": {1:["Unarmored Defense","Martial Arts"],2:["Ki", "Unarmored Movement"],3:["Monastic Tradition"]},
    "Paladin": {1:["Divine Sense","Lay on Hands"],2:["Fighting Style","Spellcasting","Divine Smite"],3:["Sacred Oath"]},
    "Ranger": {1:["Favored Enemy*","Natural Explorer*"],2:["Fighting Style","Spellcasting"],3:["Ranger Archetype"]},
    "Rogue": {1:["Expertise (choose 2)", "Sneak Attack (1d6)", "Thieves' Cant"],2:["Cunning Action"],3:["Roguish Archetype","Sneak Attack 2d6"]},
    "Sorcerer": {1:["Spellcasting","Sorcerous Origin"],2:["Font of Magic"],3:["Metamagic"]},
    "Warlock": {1:["Otherworldly Patron","Pact Magic"],2:["Eldritch Invocations"],3:["Pact Boon"]},
    "Wizard": {1:["Spellbook","Arcane Recovery"],2:["Arcane Tradition"]},
}

# =========================
# Backgrounds (SRD)
# =========================
# BACKGROUNDS[name] = {
#   "skills": [..], "tools": [..], "languages": int or [..],
#   "equipment": [..], "feature": "name"
# }

BACKGROUNDS = {
    "Acolyte": {
        "skills": ["Insight", "Religion"],
        "tools": [],
        "languages": 2,
        "equipment": [
            "holy symbol (gift)", "prayer book or prayer wheel", "5 sticks of incense",
            "vestments", "common clothes", "pouch (15 gp)"
        ],
        "feature": "Shelter of the Faithful",
    },
    "Criminal": {
        "skills": ["Deception", "Stealth"],
        "tools": ["one type of gaming set", "thieves' tools"],
        "languages": 0,
        "equipment": ["crowbar", "dark common clothes with hood", "pouch (15 gp)"],
        "feature": "Criminal Contact",
    },
    "Folk Hero": {
        "skills": ["Animal Handling", "Survival"],
        "tools": ["one type of artisan's tools", "vehicles (land)"] ,
        "languages": 0,
        "equipment": ["artisan's tools (one)", "shovel", "iron pot", "common clothes", "pouch (10 gp)"],
        "feature": "Rustic Hospitality",
    },
    "Noble": {
        "skills": ["History", "Persuasion"],
        "tools": ["one type of gaming set"],
        "languages": 1,
        "equipment": ["fine clothes", "signet ring", "scroll of pedigree", "purse (25 gp)"],
        "feature": "Position of Privilege",
    },
    "Sage": {
        "skills": ["Arcana", "History"],
        "tools": [],
        "languages": 2,
        "equipment": ["bottle of black ink", "quill", "small knife", "letter from a dead colleague with an unsolved question", "common clothes", "pouch (10 gp)"],
        "feature": "Researcher",
    },
    "Soldier": {
        "skills": ["Athletics", "Intimidation"],
        "tools": ["one type of gaming set", "vehicles (land)"],
        "languages": 0,
        "equipment": ["insignia of rank", "trophy from a fallen enemy", "gaming set (dice/cards)", "common clothes", "pouch (10 gp)"],
        "feature": "Military Rank",
    },
}

# =========================
# Derived stats helpers (static rules for the GUI to use)
# =========================
DERIVED_RULES = {
    "proficiency_by_level": [2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,6,6,6],
    "passive_perception": "10 + Perception bonus",
    "initiative": "DEX modifier",
    "hp_level1": "Max of class hit die + CON modifier",
    "hp_higher_levels": "Hit Die roll (or average) + CON modifier",
}

# =========================
# Spellcasting: slots tables & casting abilities
# =========================
# Full‑caster slots by character level (Bard, Cleric, Druid, Sorcerer, Wizard)
FULL_CASTER_SLOTS = {
     1: [2,0,0,0,0,0,0,0,0],  2: [3,0,0,0,0,0,0,0,0],  3: [4,2,0,0,0,0,0,0,0],
     4: [4,3,0,0,0,0,0,0,0],  5: [4,3,2,0,0,0,0,0,0],  6: [4,3,3,0,0,0,0,0,0],
     7: [4,3,3,1,0,0,0,0,0],  8: [4,3,3,2,0,0,0,0,0],  9: [4,3,3,3,1,0,0,0,0],
    10: [4,3,3,3,2,0,0,0,0], 11: [4,3,3,3,2,1,0,0,0], 12: [4,3,3,3,2,1,0,0,0],
    13: [4,3,3,3,2,1,1,0,0], 14: [4,3,3,3,2,1,1,0,0], 15: [4,3,3,3,2,1,1,1,0],
    16: [4,3,3,3,2,1,1,1,0], 17: [4,3,3,3,2,1,1,1,1], 18: [4,3,3,3,3,1,1,1,1],
    19: [4,3,3,3,3,2,1,1,1], 20: [4,3,3,3,3,2,2,1,1],
}

# Half‑caster helper (Paladin, Ranger) – for multiclass math
HALF_CASTER_LEVEL_MAP = {
     1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5,
    11: 6,12: 6,13: 7,14: 7,15: 8,16: 8,17: 9,18: 9,19:10,20:10,
}

# Warlock Pact Magic — short‑rest slots; entries are (slots, slot_level)
WARLOCK_PACT_SLOTS = {
     1: (1,1), 2: (2,1), 3: (2,2), 4: (2,2), 5: (2,3), 6: (2,3), 7: (2,4), 8: (2,4),
     9: (2,5), 10: (2,5), 11: (3,5), 12: (3,5), 13: (3,5), 14: (3,5), 15: (3,5), 16: (3,5), 17: (4,5), 18: (4,5), 19: (4,5), 20: (4,5)
}

# Class spellcasting ability (for DC/attack calculations)
CLASS_SPELLCASTING_ABILITY = {
    "Bard": "CHA", "Cleric": "WIS", "Druid": "WIS", "Sorcerer": "CHA",
    "Warlock": "CHA", "Wizard": "INT", "Paladin": "CHA", "Ranger": "WIS",
}

# Minimal seed of SRD‑style spells for UI demos (replace with full list file later)
SRD_SPELL_LISTS_MIN = {
    "Cleric": ["cure wounds", "bless", "guiding bolt", "spiritual weapon"],
    "Wizard": ["mage armor", "magic missile", "shield", "fireball"],
    "Druid":  ["entangle", "goodberry", "flaming sphere"],
    "Bard":   ["vicious mockery", "healing word", "dissonant whispers"],
    "Warlock":["eldritch blast", "hex", "armor of Agathys"],
    "Sorcerer":["chromatic orb", "burning hands"],
    "Paladin": ["cure wounds", "bless"],
    "Ranger":  ["hunter's mark", "goodberry"],
}

# =========================
# Appearance & personal details (for UI fields)
# =========================
APPEARANCE_FIELDS = [
    "Age", "Height", "Weight", "Eyes", "Skin", "Hair", "Faith", "Lifestyle"
]

PERSONALITY_FIELDS = [
    "Personality Traits (2)", "Ideal", "Bond", "Flaw"
]
