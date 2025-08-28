export interface CharacterMeta {
  name: string;
  player: string;
  race: string;
  subrace?: string;
  class: string;
  level: number;
  background: string;
  alignment?: string;
}

export interface Abilities {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

export interface RaceFeature {
  name: string;
  description: string;
}

export interface RaceData {
  name: string;
  features: RaceFeature[];
  abilityScoreIncrease: Partial<Abilities>;
  speed: number;
  darkvision?: number;
  languages: string[];
  subraces?: SubraceData[];
}

export interface SubraceData {
  name: string;
  features: RaceFeature[];
  abilityScoreIncrease?: Partial<Abilities>;
  speed?: number;
  darkvision?: number;
  additionalLanguages?: string[];
}

export interface ClassData {
  name: string;
  hitDie: number;
  savingThrows: (keyof Abilities)[];
  skillChoices: {
    choose: number;
    from: string[];
  };
  equipmentChoices: EquipmentChoice[];
  spellcasting?: {
    ability: keyof Abilities;
    progression: 'full' | 'half' | 'warlock';
  };
}

export interface EquipmentChoice {
  choose: number;
  options: string[];
}

export interface BackgroundData {
  name: string;
  skills: string[];
  languages: number | string[];
  tools: string[];
  equipment: string[];
  feature: {
    name: string;
    description: string;
  };
}

export interface SpellData {
  name: string;
  level: number;
  school: string;
  description: string;
}

export interface Character {
  meta: CharacterMeta;
  baseAbilities: Abilities;
  abilities: Abilities;
  raceBlock: {
    race: RaceData;
    subrace?: SubraceData;
    appliedASI: Partial<Abilities>;
    speed: number;
    darkvision?: number;
    languages: string[];
    features: RaceFeature[];
  };
  classBlock: {
    class: ClassData;
    savingThrows: (keyof Abilities)[];
    hitDie: number;
    chosenSkills: string[];
    chosenEquipment: { [choiceIndex: number]: string };
  };
  backgroundBlock: {
    background: BackgroundData;
    skills: string[];
    tools: string[];
    languages: string[];
    feature: { name: string; description: string };
    equipment: string[];
  };
  skills: { [skill: string]: number };
  hp: {
    max: number;
    current: number;
    temp: number;
    hitDie: number;
  };
  ac: number;
  speed: number;
  initiative: number;
  passivePerception: number;
  spells?: {
    castingAbility: keyof Abilities;
    saveDC: number;
    attackBonus: number;
    chosenSpells: SpellData[];
    slots?: { [level: number]: number };
  };
  inventory: string[];
  languages: string[];
  notes: string;
  appearance: string;
  personality: string;
  schemaVersion: number;
}

export interface ValidationError {
  step: string;
  field: string;
  message: string;
}

export interface CharacterValidation {
  isValid: boolean;
  errors: ValidationError[];
}

export type AbilityGenerationMethod = 'pointBuy' | 'standardArray' | 'manual';

export interface AbilityState {
  method: AbilityGenerationMethod;
  pointsRemaining?: number;
  standardArrayAssigned?: { [value: number]: keyof Abilities | null };
  flexibleASI?: {
    race: string;
    choices: [keyof Abilities, keyof Abilities] | null;
  };
}