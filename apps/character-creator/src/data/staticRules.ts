// D&D 5e Static Rules and SRD-leaning data (ported from srd_data.txt)

import { RaceData, ClassData, BackgroundData, SpellData } from '@/types/character';

export const ABILITIES = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'] as const;

export const SKILLS_TO_ABILITIES: { [skill: string]: typeof ABILITIES[number] } = {
  'acrobatics': 'dexterity',
  'animal handling': 'wisdom',
  'arcana': 'intelligence',
  'athletics': 'strength',
  'deception': 'charisma',
  'history': 'intelligence',
  'insight': 'wisdom',
  'intimidation': 'charisma',
  'investigation': 'intelligence',
  'medicine': 'wisdom',
  'nature': 'intelligence',
  'perception': 'wisdom',
  'performance': 'charisma',
  'persuasion': 'charisma',
  'religion': 'intelligence',
  'sleight of hand': 'dexterity',
  'stealth': 'dexterity',
  'survival': 'wisdom'
};

export const ALIGNMENTS = [
  'Lawful Good', 'Neutral Good', 'Chaotic Good',
  'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
  'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
];

export const POINT_BUY_COSTS: { [score: number]: number } = {
  8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
};

export const STANDARD_ARRAY = [15, 14, 13, 12, 10, 8];

export const PROFICIENCY_BONUS: { [level: number]: number } = {
  1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
  9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5, 16: 5,
  17: 6, 18: 6, 19: 6, 20: 6
};

// Helper to build feature entries from summary strings
const f = (name: string, description?: string) => ({ name, description: description || name });

export const RACES: RaceData[] = [
  // Dragonborn (SRD lineage presentation)
  {
    name: 'Dragonborn',
    features: [
      f('Draconic Ancestry', 'Choose a type; determines breath & damage'),
      f('Breath Weapon', 'Action; DC 8 + CON mod + prof; 2d6 at 1st'),
      f('Damage Resistance', 'Resistance to your ancestry’s damage')
    ],
    abilityScoreIncrease: { strength: 2, charisma: 1 },
    speed: 30,
    languages: ['Common', 'Draconic'],
    subraces: [
      { name: 'Chromatic Dragonborn', features: [f('Chromatic Ancestry', 'Black/Blue/Green/Red/White: acid/lightning/poison/fire/cold')] },
      { name: 'Metallic Dragonborn', features: [f('Metallic Ancestry', 'Brass/Bronze/Copper/Gold/Silver: fire/lightning/acid/fire/cold')] }
    ]
  },
  // Dwarf
  {
    name: 'Dwarf',
    features: [
      f('Dwarven Resilience', 'Advantage vs. poison; resistance to poison'),
      f('Dwarven Combat Training', 'Battleaxe, handaxe, light hammer, warhammer'),
      f('Tool Proficiency', 'Smith’s, brewer’s, or mason’s tools'),
      f('Stonecunning', 'Double proficiency on stonework History'),
      f('Heavy Armor Speed', 'Speed not reduced by heavy armor')
    ],
    abilityScoreIncrease: { constitution: 2 },
    speed: 25,
    darkvision: 60,
    languages: ['Common', 'Dwarvish'],
    subraces: [
      { name: 'Hill Dwarf', features: [f('Dwarven Toughness', '+1 HP per level')], abilityScoreIncrease: { wisdom: 1 } },
      { name: 'Mountain Dwarf', features: [f('Dwarven Armor Training', 'Light & medium armor')], abilityScoreIncrease: { strength: 2 } }
    ]
  },
  // Elf
  {
    name: 'Elf',
    features: [
      f('Keen Senses', 'Perception proficiency'),
      f('Fey Ancestry', 'Advantage vs. charm; immune to magical sleep'),
      f('Trance', '4-hour meditation counts as 8-hour sleep')
    ],
    abilityScoreIncrease: { dexterity: 2 },
    speed: 30,
    darkvision: 60,
    languages: ['Common', 'Elvish'],
    subraces: [
      {
        name: 'High Elf',
        features: [
          f('Elf Weapon Training', 'Longsword, shortsword, shortbow, longbow'),
          f('Cantrip', 'One wizard cantrip (INT)'),
          f('Extra Language', 'One of your choice')
        ],
        abilityScoreIncrease: { intelligence: 1 }
      },
      {
        name: 'Wood Elf',
        features: [
          f('Elf Weapon Training', 'Longsword, shortsword, shortbow, longbow'),
          f('Fleet of Foot', 'Speed 35 ft'),
          f('Mask of the Wild', 'Hide when lightly obscured')
        ],
        speed: 35,
        abilityScoreIncrease: { wisdom: 1 }
      },
      {
        name: 'Drow',
        features: [
          f('Sunlight Sensitivity', 'Disadvantage on attacks & Perception relying on sight in sunlight'),
          f('Drow Magic', 'Dancing lights; later faerie fire, darkness'),
          f('Drow Weapon Training', 'Rapiers, shortswords, hand crossbows')
        ],
        darkvision: 120,
        abilityScoreIncrease: { charisma: 1 }
      }
    ]
  },
  // Gnome
  {
    name: 'Gnome',
    features: [f('Gnome Cunning', 'Advantage on INT/WIS/CHA saves vs. magic')],
    abilityScoreIncrease: { intelligence: 2 },
    speed: 25,
    darkvision: 60,
    languages: ['Common', 'Gnomish'],
    subraces: [
      { name: 'Forest Gnome', features: [f('Natural Illusionist', 'Minor illusion cantrip (INT)'), f('Speak with Small Beasts', 'Limited communication')], abilityScoreIncrease: { dexterity: 1 } },
      { name: 'Rock Gnome', features: [f('Artificer’s Lore', 'Double proficiency History for magic/tech'), f('Tinker', 'Tinker’s tools; Tiny devices')], abilityScoreIncrease: { constitution: 1 } }
    ]
  },
  // Half-Elf
  {
    name: 'Half-Elf',
    features: [f('Fey Ancestry', 'Advantage vs. charm; immune to magical sleep'), f('Skill Versatility', 'Choose two skills')],
    abilityScoreIncrease: { charisma: 2 }, // plus flexible +1/+1 handled by UI
    speed: 30,
    darkvision: 60,
    languages: ['Common', 'Elvish', 'Choice'],
    subraces: [
      { name: 'High Half-Elf', features: [f('High Elf Leanings', '+1 INT')], abilityScoreIncrease: { intelligence: 1 } },
      { name: 'Wood Half-Elf', features: [f('Wood Elf Leanings', '+1 WIS')], abilityScoreIncrease: { wisdom: 1 } }
    ]
  },
  // Half-Orc
  {
    name: 'Half-Orc',
    features: [f('Menacing', 'Intimidation proficiency'), f('Relentless Endurance', 'Drop to 0 -> 1 HP once per long rest'), f('Savage Attacks', 'Extra die on melee crit')],
    abilityScoreIncrease: { strength: 2, constitution: 1 },
    speed: 30,
    darkvision: 60,
    languages: ['Common', 'Orc']
  },
  // Halfling
  {
    name: 'Halfling',
    features: [f('Lucky', 'Reroll 1 on d20 (must keep new roll)'), f('Brave', 'Advantage on saves vs. frightened'), f('Halfling Nimbleness', 'Move through larger creatures’ spaces')],
    abilityScoreIncrease: { dexterity: 2 },
    speed: 25,
    languages: ['Common', 'Halfling'],
    subraces: [
      { name: 'Lightfoot', features: [f('Naturally Stealthy')], abilityScoreIncrease: { charisma: 1 } },
      { name: 'Stout', features: [f('Stout Resilience', 'Advantage vs. poison; resistance')], abilityScoreIncrease: { constitution: 1 } }
    ]
  },
  // Human
  {
    name: 'Human',
    features: [],
    abilityScoreIncrease: { strength: 1, dexterity: 1, constitution: 1, intelligence: 1, wisdom: 1, charisma: 1 },
    speed: 30,
    languages: ['Common', 'Choice'],
    subraces: [
      { name: 'Standard Human', features: [f('All Abilities +1')] },
      { name: 'Variant Human', features: [f('Flexible Ability Increases', '+1 to two abilities, one skill, one feat')], abilityScoreIncrease: {} }
    ]
  },
  // Tiefling
  {
    name: 'Tiefling',
    features: [f('Hellish Resistance', 'Fire resistance'), f('Infernal Legacy', 'Thaumaturgy; later hellish rebuke, darkness')],
    abilityScoreIncrease: { charisma: 2, intelligence: 1 },
    speed: 30,
    darkvision: 60,
    languages: ['Common', 'Infernal'],
    subraces: [
      { name: 'Infernal Tiefling', features: [f('Diabolic Bloodlines')] },
      { name: 'Abyssal Tiefling', features: [f('Chaotic Demonic Influence')] }
    ]
  },
  // Non-SRD extensions (labeled)
  { name: 'Aasimar', features: [f('Non-SRD Lineage')], abilityScoreIncrease: {}, speed: 30, darkvision: 60, languages: ['Common'], subraces: [
    { name: 'Protector Aasimar', features: [f('Radiant guardians', 'Luminous flight in bursts')] },
    { name: 'Scourge Aasimar', features: [f('Burning zeal', 'Searing aura of light')] }
  ]},
  { name: 'Goliath', features: [f('Non-SRD Lineage')], abilityScoreIncrease: {}, speed: 30, languages: ['Common'], subraces: [
    { name: 'Stoneborn Goliath', features: [f('Granite-skinned mountaineers')] },
    { name: 'Stormborn Goliath', features: [f('Thunder-scarred peak-clans')] }
  ]},
  { name: 'Orc', features: [f('Non-SRD Lineage')], abilityScoreIncrease: {}, speed: 30, darkvision: 60, languages: ['Common'], subraces: [
    { name: 'Gray Orc', features: [f('Wandering plains tribes')] },
    { name: 'Orog', features: [f('Deep-delving orcs bred for war')] }
  ]}
];

// Class core: hit die, saves, skills, equipment and spellcasting progression
const CLASS_HIT_DIE: { [cls: string]: number } = {
  Barbarian: 12,
  Fighter: 10, Paladin: 10, Ranger: 10,
  Bard: 8, Cleric: 8, Druid: 8, Monk: 8, Rogue: 8, Warlock: 8,
  Sorcerer: 6, Wizard: 6,
};

const CLASS_SAVE_THROWS: { [cls: string]: any } = {
  Barbarian: ['strength', 'constitution'],
  Bard: ['dexterity', 'charisma'],
  Cleric: ['wisdom', 'charisma'],
  Druid: ['intelligence', 'wisdom'],
  Fighter: ['strength', 'constitution'],
  Monk: ['strength', 'dexterity'],
  Paladin: ['wisdom', 'charisma'],
  Ranger: ['strength', 'dexterity'],
  Rogue: ['dexterity', 'intelligence'],
  Sorcerer: ['constitution', 'charisma'],
  Warlock: ['wisdom', 'charisma'],
  Wizard: ['intelligence', 'wisdom'],
};

const CLASS_SKILL_CHOICES = {
  Barbarian: { choose: 2, from: ['animal handling','athletics','intimidation','nature','perception','survival'] },
  Bard:      { choose: 3, from: Object.keys(SKILLS_TO_ABILITIES) },
  Cleric:    { choose: 2, from: ['history','insight','medicine','persuasion','religion'] },
  Druid:     { choose: 2, from: ['arcana','animal handling','insight','medicine','nature','perception','religion','survival'] },
  Fighter:   { choose: 2, from: ['acrobatics','animal handling','athletics','history','insight','intimidation','perception','survival'] },
  Monk:      { choose: 2, from: ['acrobatics','athletics','history','insight','religion','stealth'] },
  Paladin:   { choose: 2, from: ['athletics','insight','intimidation','medicine','persuasion','religion'] },
  Ranger:    { choose: 3, from: ['animal handling','athletics','insight','investigation','nature','perception','stealth','survival'] },
  Rogue:     { choose: 4, from: ['acrobatics','athletics','deception','insight','intimidation','investigation','perception','performance','persuasion','sleight of hand','stealth'] },
  Sorcerer:  { choose: 2, from: ['arcana','deception','insight','intimidation','persuasion','religion'] },
  Warlock:   { choose: 2, from: ['arcana','deception','history','intimidation','investigation','nature','religion'] },
  Wizard:    { choose: 2, from: ['arcana','history','insight','investigation','medicine','religion'] },
};

const CLASS_STARTING_EQUIPMENT: { [cls: string]: string[][] } = {
  Barbarian: [[ 'a greataxe','any martial melee weapon' ], [ 'two handaxes','any simple weapon' ], ["an explorer's pack"], ['four javelins']],
  Bard: [[ 'a rapier','a longsword','a simple weapon' ], ["a diplomat's pack","an entertainer's pack"], ['a lute','any musical instrument'], ['leather armor','dagger']],
  Cleric: [[ 'a mace','a warhammer (if proficient)' ], ['scale mail','leather armor','chain mail (if proficient)'], [ 'a light crossbow and 20 bolts','any simple weapon' ], ["a priest's pack","an explorer's pack"], ['a shield'], ['a holy symbol']],
  Druid: [[ 'a wooden shield','any simple weapon' ], [ 'a scimitar','any simple melee weapon' ], ['a druidic focus'], ["an explorer's pack"], ['leather armor']],
  Fighter: [[ 'chain mail','leather armor, longbow, and 20 arrows' ], [ 'a martial weapon and a shield','two martial weapons' ], [ 'a light crossbow and 20 bolts','two handaxes' ], ["a dungeoneer's pack","an explorer's pack"]],
  Monk: [[ 'a shortsword','any simple weapon' ], ["a dungeoneer's pack","an explorer's pack"], ['10 darts']],
  Paladin: [[ 'a martial weapon and a shield','two martial weapons' ], [ 'five javelins','any simple melee weapon' ], ["a priest's pack","an explorer's pack"], ['chain mail'], ['a holy symbol']],
  Ranger: [[ 'scale mail','leather armor' ], [ 'two shortswords','two simple melee weapons' ], ["a dungeoneer's pack","an explorer's pack"], ['a longbow and a quiver of 20 arrows']],
  Rogue: [[ 'a rapier','a shortsword' ], [ 'a shortbow and quiver of 20 arrows','a shortsword' ], ["a burglar's pack","a dungeoneer's pack","an explorer's pack"], ['leather armor','two daggers',"thieves' tools"]],
  Sorcerer: [[ 'a light crossbow and 20 bolts','any simple weapon' ], [ 'a component pouch','an arcane focus' ], ["a dungeoneer's pack","an explorer's pack"], ['two daggers']],
  Warlock: [[ 'a light crossbow and 20 bolts','any simple weapon' ], [ 'a component pouch','an arcane focus' ], ["a scholar's pack","a dungeoneer's pack"], ['leather armor','any simple weapon','two daggers']],
  Wizard: [[ 'a quarterstaff','a dagger' ], [ 'a component pouch','an arcane focus' ], ["a scholar's pack","an explorer's pack"], ['a spellbook']],
};

export const CLASSES: ClassData[] = (
  [
    'Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard'
  ] as const
).map((name) => {
  const spellcasting: ClassData['spellcasting'] | undefined =
    name === 'Bard' || name === 'Cleric' || name === 'Druid' || name === 'Sorcerer' || name === 'Wizard'
      ? { ability: name === 'Wizard' ? 'intelligence' : name === 'Cleric' || name === 'Druid' ? 'wisdom' : 'charisma', progression: 'full' }
      : name === 'Paladin' || name === 'Ranger'
      ? { ability: name === 'Paladin' ? 'charisma' : 'wisdom', progression: 'half' }
      : name === 'Warlock'
      ? { ability: 'charisma', progression: 'warlock' }
      : undefined;

  return {
    name,
    hitDie: CLASS_HIT_DIE[name],
    savingThrows: CLASS_SAVE_THROWS[name],
    skillChoices: CLASS_SKILL_CHOICES[name as keyof typeof CLASS_SKILL_CHOICES],
    equipmentChoices: CLASS_STARTING_EQUIPMENT[name].map((options) => ({ choose: 1, options })),
    spellcasting,
  } as ClassData;
});

export const BACKGROUNDS: BackgroundData[] = [
  {
    name: 'Acolyte',
    skills: ['insight', 'religion'],
    languages: 2,
    tools: [],
    equipment: [
      'holy symbol (gift)', 'prayer book or prayer wheel', '5 sticks of incense',
      'vestments', 'common clothes', 'pouch (15 gp)'
    ],
    feature: {
      name: 'Shelter of the Faithful',
      description: 'You and your companions can receive free healing and care at temples, shrines, and other established presences of your faith.'
    }
  },
  {
    name: 'Criminal',
    skills: ['deception', 'stealth'],
    languages: 0,
    tools: ["one type of gaming set", "thieves' tools"],
    equipment: ['crowbar', 'dark common clothes with hood', 'pouch (15 gp)'],
    feature: { name: 'Criminal Contact', description: 'You have a reliable and trustworthy contact who acts as your liaison to a network of other criminals.' }
  },
  {
    name: 'Folk Hero',
    skills: ['animal handling', 'survival'],
    languages: 0,
    tools: ["one type of artisan's tools", 'vehicles (land)'],
    equipment: ["artisan's tools (one)", 'shovel', 'iron pot', 'common clothes', 'pouch (10 gp)'],
    feature: { name: 'Rustic Hospitality', description: 'Since you come from the ranks of the common folk, you fit in among them with ease.' }
  },
  {
    name: 'Noble',
    skills: ['history', 'persuasion'],
    languages: 1,
    tools: ["one type of gaming set"],
    equipment: ['fine clothes', 'signet ring', 'scroll of pedigree', 'purse (25 gp)'],
    feature: { name: 'Position of Privilege', description: 'People are inclined to think the best of you.' }
  },
  {
    name: 'Sage',
    skills: ['arcana', 'history'],
    languages: 2,
    tools: [],
    equipment: ['bottle of black ink', 'quill', 'small knife', 'letter from a dead colleague with an unsolved question', 'common clothes', 'pouch (10 gp)'],
    feature: { name: 'Researcher', description: 'When you attempt to learn or recall a piece of lore, if you do not know that information, you often know where and from whom you can obtain it.' }
  },
  {
    name: 'Soldier',
    skills: ['athletics', 'intimidation'],
    languages: 0,
    tools: ["one type of gaming set", 'vehicles (land)'],
    equipment: ['insignia of rank', 'trophy from a fallen enemy', 'gaming set (dice/cards)', 'common clothes', 'pouch (10 gp)'],
    feature: { name: 'Military Rank', description: 'You have a military rank from your career as a soldier.' }
  }
];

// Minimal seed of SRD-style spells (class-agnostic list for current UI)
export const SPELLS: SpellData[] = [
  { name: 'Fire Bolt', level: 0, school: 'Evocation', description: 'You hurl a mote of fire.' },
  { name: 'Mage Hand', level: 0, school: 'Conjuration', description: 'A spectral, floating hand appears within range.' },
  { name: 'Magic Missile', level: 1, school: 'Evocation', description: 'Create glowing darts of magical force.' },
  { name: 'Shield', level: 1, school: 'Abjuration', description: 'An invisible barrier of magical force protects you.' }
];

// Spell slots: full casters table (levels 1-20)
export const SPELL_SLOTS_FULL_CASTER: { [level: number]: number[] } = {
  1: [2,0,0,0,0,0,0,0,0],  2: [3,0,0,0,0,0,0,0,0],  3: [4,2,0,0,0,0,0,0,0],
  4: [4,3,0,0,0,0,0,0,0],  5: [4,3,2,0,0,0,0,0,0],  6: [4,3,3,0,0,0,0,0,0],
  7: [4,3,3,1,0,0,0,0,0],  8: [4,3,3,2,0,0,0,0,0],  9: [4,3,3,3,1,0,0,0,0],
  10:[4,3,3,3,2,0,0,0,0], 11:[4,3,3,3,2,1,0,0,0], 12:[4,3,3,3,2,1,0,0,0],
  13:[4,3,3,3,2,1,1,0,0], 14:[4,3,3,3,2,1,1,0,0], 15:[4,3,3,3,2,1,1,1,0],
  16:[4,3,3,3,2,1,1,1,0], 17:[4,3,3,3,2,1,1,1,1], 18:[4,3,3,3,3,1,1,1,1],
  19:[4,3,3,3,3,2,1,1,1], 20:[4,3,3,3,3,2,2,1,1],
};

// Half-caster level mapping (Paladin, Ranger) for computing slots
export const HALF_CASTER_EFFECTIVE_LEVEL: { [level: number]: number } = {
  1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5,
  11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10,
};

// Warlock pact magic slots: maps level -> [slots, slotLevel]
export const WARLOCK_PACT_SLOTS: { [level: number]: [number, number] } = {
  1:[1,1], 2:[2,1], 3:[2,2], 4:[2,2], 5:[2,3], 6:[2,3], 7:[2,4], 8:[2,4], 9:[2,5], 10:[2,5],
  11:[3,5], 12:[3,5], 13:[3,5], 14:[3,5], 15:[3,5], 16:[3,5], 17:[4,5], 18:[4,5], 19:[4,5], 20:[4,5]
};

export const LANGUAGES = [
  'Common', 'Dwarvish', 'Elvish', 'Giant', 'Gnomish', 'Goblin', 'Halfling', 'Orc',
  'Abyssal', 'Celestial', 'Draconic', 'Deep Speech', 'Infernal', 'Primordial', 'Sylvan', 'Undercommon'
];

// Minimal SRD-style per-class spell lists (names)
export const CLASS_SPELL_LISTS_MIN: { [cls: string]: string[] } = {
  Cleric: ['cure wounds', 'bless', 'guiding bolt', 'spiritual weapon'],
  Wizard: ['mage armor', 'magic missile', 'shield', 'fireball'],
  Druid: ['entangle', 'goodberry', 'flaming sphere'],
  Bard: ['vicious mockery', 'healing word', 'dissonant whispers'],
  Warlock: ['eldritch blast', 'hex', 'armor of Agathys'],
  Sorcerer: ['chromatic orb', 'burning hands'],
  Paladin: ['cure wounds', 'bless'],
  Ranger: ["hunter's mark", 'goodberry']
};

// Suggested fields to prompt richer descriptions
export const APPEARANCE_FIELDS = ['Age', 'Height', 'Weight', 'Eyes', 'Skin', 'Hair', 'Faith', 'Lifestyle'];
export const PERSONALITY_FIELDS = ['Personality Traits (2)', 'Ideal', 'Bond', 'Flaw'];
