// D&D 5e Static Rules and Seed Data

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

export const POINT_BUY_COSTS: { [score: number]: number } = {
  8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
};

export const STANDARD_ARRAY = [15, 14, 13, 12, 10, 8];

export const PROFICIENCY_BONUS: { [level: number]: number } = {
  1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
  9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5, 16: 5,
  17: 6, 18: 6, 19: 6, 20: 6
};

export const RACES: RaceData[] = [
  {
    name: 'Human',
    features: [
      { name: 'Versatile', description: 'Humans are adaptable and ambitious.' }
    ],
    abilityScoreIncrease: { strength: 1, dexterity: 1, constitution: 1, intelligence: 1, wisdom: 1, charisma: 1 },
    speed: 30,
    languages: ['Common'],
    subraces: [
      {
        name: 'Variant Human',
        features: [
          { name: 'Skills', description: 'You gain proficiency in one skill of your choice.' },
          { name: 'Feat', description: 'You gain one feat of your choice.' }
        ],
        abilityScoreIncrease: { /* flexible: choose any 2 different */ },
        additionalLanguages: []
      }
    ]
  },
  {
    name: 'Elf',
    features: [
      { name: 'Darkvision', description: 'You have superior vision in dark conditions.' },
      { name: 'Fey Ancestry', description: 'You have advantage on saving throws against being charmed.' },
      { name: 'Trance', description: 'You don\'t need to sleep and can\'t be forced to sleep.' }
    ],
    abilityScoreIncrease: { dexterity: 2 },
    speed: 30,
    darkvision: 60,
    languages: ['Common', 'Elvish'],
    subraces: [
      {
        name: 'High Elf',
        features: [
          { name: 'Cantrip', description: 'You know one cantrip of your choice from the wizard spell list.' },
          { name: 'Elf Weapon Training', description: 'You have proficiency with longswords, shortbows, longbows, and shortbows.' }
        ],
        abilityScoreIncrease: { intelligence: 1 },
        additionalLanguages: []
      },
      {
        name: 'Wood Elf',
        features: [
          { name: 'Elf Weapon Training', description: 'You have proficiency with longswords, shortbows, longbows, and shortbows.' },
          { name: 'Fleet of Foot', description: 'Your base walking speed increases to 35 feet.' },
          { name: 'Mask of the Wild', description: 'You can attempt to hide even when only lightly obscured by natural phenomena.' }
        ],
        abilityScoreIncrease: { wisdom: 1 },
        speed: 35
      }
    ]
  },
  {
    name: 'Dwarf',
    features: [
      { name: 'Darkvision', description: 'You have superior vision in dark conditions.' },
      { name: 'Dwarven Resilience', description: 'You have advantage on saving throws against poison.' },
      { name: 'Stonecunning', description: 'You can add twice your proficiency bonus to History checks related to stonework.' }
    ],
    abilityScoreIncrease: { constitution: 2 },
    speed: 25,
    darkvision: 60,
    languages: ['Common', 'Dwarvish'],
    subraces: [
      {
        name: 'Hill Dwarf',
        features: [
          { name: 'Dwarven Toughness', description: 'Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.' }
        ],
        abilityScoreIncrease: { wisdom: 1 }
      },
      {
        name: 'Mountain Dwarf',
        features: [
          { name: 'Armor Proficiency', description: 'You have proficiency with light and medium armor.' }
        ],
        abilityScoreIncrease: { strength: 2 }
      }
    ]
  }
];

export const CLASSES: ClassData[] = [
  {
    name: 'Fighter',
    hitDie: 10,
    savingThrows: ['strength', 'constitution'],
    skillChoices: {
      choose: 2,
      from: ['acrobatics', 'animal handling', 'athletics', 'history', 'insight', 'intimidation', 'perception', 'survival']
    },
    equipmentChoices: [
      {
        choose: 1,
        options: ['Chain mail', 'Leather armor, longbow, and 20 arrows']
      },
      {
        choose: 1,
        options: ['A martial weapon and a shield', 'Two martial weapons']
      },
      {
        choose: 1,
        options: ['A light crossbow and 20 bolts', 'Two handaxes']
      }
    ]
  },
  {
    name: 'Wizard',
    hitDie: 6,
    savingThrows: ['intelligence', 'wisdom'],
    skillChoices: {
      choose: 2,
      from: ['arcana', 'history', 'insight', 'investigation', 'medicine', 'religion']
    },
    equipmentChoices: [
      {
        choose: 1,
        options: ['A quarterstaff', 'A dagger']
      },
      {
        choose: 1,
        options: ['A component pouch', 'An arcane focus']
      }
    ],
    spellcasting: {
      ability: 'intelligence',
      progression: 'full'
    }
  },
  {
    name: 'Rogue',
    hitDie: 8,
    savingThrows: ['dexterity', 'intelligence'],
    skillChoices: {
      choose: 4,
      from: ['acrobatics', 'athletics', 'deception', 'insight', 'intimidation', 'investigation', 'perception', 'performance', 'persuasion', 'sleight of hand', 'stealth']
    },
    equipmentChoices: [
      {
        choose: 1,
        options: ['A rapier', 'A shortsword']
      },
      {
        choose: 1,
        options: ['A shortbow and quiver of 20 arrows', 'A shortsword']
      }
    ]
  }
];

export const BACKGROUNDS: BackgroundData[] = [
  {
    name: 'Acolyte',
    skills: ['insight', 'religion'],
    languages: 2,
    tools: [],
    equipment: [
      'A holy symbol',
      'A prayer book or prayer wheel',
      '5 sticks of incense',
      'Vestments',
      'A set of common clothes',
      'A pouch containing 15 gp'
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
    tools: ['Thieves\' tools', 'Gaming set'],
    equipment: [
      'A crowbar',
      'A set of dark common clothes including a hood',
      'A pouch containing 15 gp'
    ],
    feature: {
      name: 'Criminal Contact',
      description: 'You have a reliable and trustworthy contact who acts as your liaison to a network of other criminals.'
    }
  },
  {
    name: 'Folk Hero',
    skills: ['animal handling', 'survival'],
    languages: 0,
    tools: ['Artisan\'s tools', 'Vehicles (land)'],
    equipment: [
      'A set of artisan\'s tools',
      'A shovel',
      'A set of artisan\'s tools',
      'A set of common clothes',
      'A pouch containing 10 gp'
    ],
    feature: {
      name: 'Rustic Hospitality',
      description: 'Since you come from the ranks of the common folk, you fit in among them with ease.'
    }
  }
];

export const SPELLS: SpellData[] = [
  {
    name: 'Fire Bolt',
    level: 0,
    school: 'Evocation',
    description: 'You hurl a mote of fire at a creature or object within range.'
  },
  {
    name: 'Mage Hand',
    level: 0,
    school: 'Conjuration', 
    description: 'A spectral, floating hand appears at a point you choose within range.'
  },
  {
    name: 'Magic Missile',
    level: 1,
    school: 'Evocation',
    description: 'You create three glowing darts of magical force.'
  },
  {
    name: 'Shield',
    level: 1,
    school: 'Abjuration',
    description: 'An invisible barrier of magical force appears and protects you.'
  }
];

export const SPELL_SLOTS_FULL_CASTER: { [level: number]: number[] } = {
  1: [2, 0, 0, 0, 0, 0, 0, 0, 0],
  2: [3, 0, 0, 0, 0, 0, 0, 0, 0],
  3: [4, 2, 0, 0, 0, 0, 0, 0, 0],
  // ... continue for all levels
};

export const LANGUAGES = [
  'Common', 'Dwarvish', 'Elvish', 'Giant', 'Gnomish', 'Goblin', 'Halfling', 'Orc',
  'Abyssal', 'Celestial', 'Draconic', 'Deep Speech', 'Infernal', 'Primordial', 'Sylvan', 'Undercommon'
];