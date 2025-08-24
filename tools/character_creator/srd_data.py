# https://www.dndbeyond.com/srd

# Classes
CLASSES = [
    "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
    "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"
]

# Races
RACES = {
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

# Subraces
SUBRACES = {
    "Dwarf": ["Hill Dwarf", "Mountain Dwarf"],
    "Elf": ["High Elf", "Wood Elf", "Drow"],
    "Gnome": ["Forest Gnome", "Rock Gnome"],
    "Halfling": ["Lightfoot", "Stout"],
}

# Alignment
ALIGNMENTS = [
    "Lawful Good", "Neutral Good", "Chaotic Good",
    "Lawful Neutral", "True Neutral", "Chaotic Neutral",
    "Lawful Evil", "Neutral Evil", "Chaotic Evil"
]

# Abilities
ABILITIES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

# Skills
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

# Hit die
CLASS_HIT_DIE = {
    "Barbarian": "1d12",
    "Fighter": "1d10", "Paladin": "1d10", "Ranger": "1d10",
    "Bard": "1d8", "Cleric": "1d8", "Druid": "1d8", "Monk": "1d8", "Rogue": "1d8", "Warlock": "1d8",
    "Sorcerer": "1d6", "Wizard": "1d6",
}

# Save throws
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

# Score generation
STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
POINT_BUY_MIN = 8
POINT_BUY_MAX = 15
POINT_BUY_BUDGET = 27
POINT_BUY_COST = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}