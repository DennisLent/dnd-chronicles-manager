import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Character, SpellData } from '@/types/character';
import { CLASSES, SPELLS, SPELL_SLOTS_FULL_CASTER, HALF_CASTER_EFFECTIVE_LEVEL, WARLOCK_PACT_SLOTS, CLASS_SPELL_LISTS_MIN } from '@/data/staticRules';
import { Sparkles, Plus, BookOpen, Wand2 } from 'lucide-react';

interface SpellsStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onNext: () => void;
  onPrevious: () => void;
}

export const SpellsStep: React.FC<SpellsStepProps> = ({
  character,
  updateCharacter,
  onNext,
  onPrevious
}) => {
  const [customSpellDialog, setCustomSpellDialog] = useState(false);
  const [customSpell, setCustomSpell] = useState({
    name: '',
    level: 0,
    school: '',
    description: ''
  });

  const classData = CLASSES.find(c => c.name === character.meta?.class);
  const level = character.meta?.level || 1;
  const chosenSpells = character.spells?.chosenSpells || [];
  const castingAbility = classData?.spellcasting?.ability;
  const abilityMod = castingAbility ? Math.floor((character.abilities?.[castingAbility] || 10 - 10) / 2) : 0;
  const proficiencyBonus = Math.ceil(level / 4) + 1;

  // Determine if spells are available
  const hasSpellcasting = classData?.spellcasting !== undefined;
  const canCastSpells = hasSpellcasting && (
    classData.spellcasting?.progression === 'full' || 
    (classData.spellcasting?.progression === 'half' && level >= 2) ||
    (classData.spellcasting?.progression === 'warlock' && level >= 1)
  );

  const spellSlots = (() => {
    if (!hasSpellcasting) return null;
    const prog = classData!.spellcasting!.progression;
    if (prog === 'full') {
      return { type: 'full' as const, slots: SPELL_SLOTS_FULL_CASTER[level] };
    }
    if (prog === 'half') {
      const eff = HALF_CASTER_EFFECTIVE_LEVEL[level];
      return { type: 'half' as const, slots: SPELL_SLOTS_FULL_CASTER[eff] };
    }
    if (prog === 'warlock') {
      const [slots, slotLevel] = WARLOCK_PACT_SLOTS[level];
      return { type: 'warlock' as const, pact: { slots, slotLevel } };
    }
    return null;
  })();

  // Limit how many leveled spells can be chosen (cantrips excluded)
  const maxLeveledSpells = (() => {
    if (!spellSlots) return 0;
    // warlock pact magic: limit equals number of pact slots
    if (spellSlots.type === 'warlock') return spellSlots.pact!.slots;
    // full/half casters: sum slots across levels
    return (spellSlots.slots || []).reduce((a, b) => a + b, 0);
  })();
  const chosenLeveledCount = chosenSpells.filter(s => s.level > 0).length;

  const handleSpellToggle = (spell: SpellData) => {
    const isSelected = chosenSpells.some(s => s.name === spell.name);
    let newSpells;
    
    if (isSelected) {
      newSpells = chosenSpells.filter(s => s.name !== spell.name);
    } else {
      if (spell.level > 0 && chosenLeveledCount >= maxLeveledSpells) {
        return; // limit reached for leveled spells
      }
      newSpells = [...chosenSpells, spell];
    }

    updateCharacter({
      spells: {
        castingAbility: castingAbility!,
        saveDC: 8 + proficiencyBonus + abilityMod,
        attackBonus: proficiencyBonus + abilityMod,
        chosenSpells: newSpells
      }
    });
  };

  const handleCustomSpellAdd = () => {
    if (!customSpell.name || !customSpell.description) return;
    
    const newSpell: SpellData = {
      name: customSpell.name,
      level: customSpell.level,
      school: customSpell.school || 'Evocation',
      description: customSpell.description
    };

    handleSpellToggle(newSpell);
    setCustomSpell({ name: '', level: 0, school: '', description: '' });
    setCustomSpellDialog(false);
  };

  const getSpellsByLevel = (level: number) => {
    const className = classData?.name || '';
    const allowed = CLASS_SPELL_LISTS_MIN[className];
    return SPELLS.filter(spell => {
      if (spell.level !== level) return false;
      if (!allowed) return true;
      return allowed.includes(spell.name.toLowerCase());
    });
  };

  if (!hasSpellcasting) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <BookOpen className="w-8 h-8 text-muted-foreground mr-3" />
            <h2 className="text-2xl font-bold">Spells</h2>
          </div>
          <Card className="p-8 bg-muted/30">
            <div className="text-center space-y-4">
              <Wand2 className="w-12 h-12 text-muted-foreground mx-auto" />
              <h3 className="text-lg font-semibold">No Spellcasting</h3>
              <p className="text-muted-foreground">
                Your {character.meta?.class} class doesn't have spellcasting abilities at this level.
              </p>
            </div>
          </Card>
        </div>
        
        <div className="flex justify-between pt-6">
          <Button variant="outline" onClick={onPrevious}>
            Previous: Equipment
          </Button>
          <Button onClick={onNext}>
            Next: Details
          </Button>
        </div>
      </div>
    );
  }

  if (!canCastSpells) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-primary mr-3" />
            <h2 className="text-2xl font-bold">Spells</h2>
          </div>
          <Card className="p-8 bg-muted/30">
            <div className="text-center space-y-4">
              <Sparkles className="w-12 h-12 text-muted-foreground mx-auto" />
              <h3 className="text-lg font-semibold">Spellcasting Locked</h3>
              <p className="text-muted-foreground">
                Your {character.meta?.class} gains spellcasting abilities at level{' '}
                {classData.spellcasting?.progression === 'half' ? '2' : '1'}.
                Current level: {level}
              </p>
            </div>
          </Card>
        </div>
        
        <div className="flex justify-between pt-6">
          <Button variant="outline" onClick={onPrevious}>
            Previous: Equipment
          </Button>
          <Button onClick={onNext}>
            Next: Details
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Sparkles className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-2xl font-bold">Spells</h2>
        </div>
        <p className="text-muted-foreground">
          Choose spells for your {character.meta?.class}. You can select from the seed list or create custom spells.
        </p>
      </div>

      {/* Spell Stats */}
      <Card className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div>
            <Label className="text-xs text-muted-foreground">Spell Save DC</Label>
            <div className="text-lg font-bold">
              {8 + proficiencyBonus + abilityMod}
            </div>
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">Spell Attack Bonus</Label>
            <div className="text-lg font-bold">
              +{proficiencyBonus + abilityMod}
            </div>
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">Casting Ability</Label>
            <div className="text-lg font-bold capitalize">
              {castingAbility}
            </div>
          </div>
        </div>
        {spellSlots && (
          <div className="mt-4 text-sm text-left">
            {spellSlots.type === 'warlock' ? (
              <div>
                <Label className="text-xs text-muted-foreground">Pact Magic</Label>
                <div>Slots: {spellSlots.pact!.slots} • Slot Level: {spellSlots.pact!.slotLevel}</div>
                <div className="text-xs text-muted-foreground mt-1">Leveled spells selected: {chosenSpells.filter(s => s.level > 0).length} / {spellSlots.pact!.slots}</div>
              </div>
            ) : (
              <div>
                <Label className="text-xs text-muted-foreground">Spell Slots by Level</Label>
                <div className="mt-1 grid grid-cols-9 gap-1 text-center">
                  {spellSlots.slots!.map((n, i) => (
                    <div key={i} className="px-2 py-1 rounded bg-muted/40">
                      <div className="text-[10px] text-muted-foreground">{i+1}</div>
                      <div className="font-semibold">{n}</div>
                    </div>
                  ))}
                </div>
                <div className="text-xs text-muted-foreground mt-1">Leveled spells selected: {chosenSpells.filter(s => s.level > 0).length} / { (spellSlots.slots || []).reduce((a,b)=>a+b,0) }</div>
              </div>
            )}
          </div>
        )}
      </Card>

      {/* Selected Spells */}
      {chosenSpells.length > 0 && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Selected Spells</h3>
          <div className="grid gap-3">
            {chosenSpells.map((spell, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-muted/30 rounded">
                <div>
                  <div className="font-medium">{spell.name}</div>
                  <div className="text-sm text-muted-foreground">
                    Level {spell.level} {spell.school}
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleSpellToggle(spell)}
                >
                  Remove
                </Button>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Available Spells */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Available Spells</h3>
          <Dialog open={customSpellDialog} onOpenChange={setCustomSpellDialog}>
            <DialogTrigger asChild>
              <Button variant="outline" size="sm">
                <Plus className="w-4 h-4 mr-2" />
                Add Custom Spell
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create Custom Spell</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="spell-name">Spell Name</Label>
                  <Input
                    id="spell-name"
                    value={customSpell.name}
                    onChange={(e) => setCustomSpell({...customSpell, name: e.target.value})}
                    placeholder="Enter spell name"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="spell-level">Level</Label>
                    <Input
                      id="spell-level"
                      type="number"
                      min="0"
                      max="9"
                      value={customSpell.level}
                      onChange={(e) => setCustomSpell({...customSpell, level: parseInt(e.target.value) || 0})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="spell-school">School</Label>
                    <Input
                      id="spell-school"
                      value={customSpell.school}
                      onChange={(e) => setCustomSpell({...customSpell, school: e.target.value})}
                      placeholder="e.g., Evocation"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="spell-description">Description</Label>
                  <Textarea
                    id="spell-description"
                    value={customSpell.description}
                    onChange={(e) => setCustomSpell({...customSpell, description: e.target.value})}
                    placeholder="Describe the spell's effects..."
                    className="min-h-20"
                  />
                </div>
                <Button onClick={handleCustomSpellAdd} className="w-full">
                  Add Spell
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="space-y-6">
          {[0, 1].map(level => (
            <div key={level} className="space-y-3">
              <h4 className="font-medium">
                {level === 0 ? 'Cantrips' : `Level ${level} Spells`}
              </h4>
              <div className="grid gap-2">
                {getSpellsByLevel(level).map((spell, index) => {
                  const isSelected = chosenSpells.some(s => s.name === spell.name);
                  const atCap = spell.level > 0 && !isSelected && chosenLeveledCount >= maxLeveledSpells;
                  return (
                    <div
                      key={index}
                      className={`p-3 border rounded transition-colors ${
                        isSelected
                          ? 'border-primary bg-primary/10'
                          : atCap ? 'border-border opacity-60 cursor-not-allowed' : 'border-border hover:border-primary/50 cursor-pointer'
                      }`}
                      onClick={() => { if (!atCap) handleSpellToggle(spell); }}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium">{spell.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {spell.school}
                          </div>
                        </div>
                        <Badge variant={isSelected ? 'default' : atCap ? 'outline' : 'secondary'}>
                          {isSelected ? 'Selected' : atCap ? 'Limit Reached' : 'Available'}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">
                        {spell.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onPrevious}>
          Previous: Equipment
        </Button>
        <Button onClick={onNext}>
          Next: Details
        </Button>
      </div>
    </div>
  );
};
