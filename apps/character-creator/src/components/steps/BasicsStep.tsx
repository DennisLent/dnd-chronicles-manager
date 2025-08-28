import React, { useState } from 'react';
import { ChevronRight, User, Crown, Briefcase } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Character } from '@/types/character';
import { RACES, CLASSES, BACKGROUNDS } from '@/data/staticRules';

interface BasicsStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onNext: () => void;
}

export const BasicsStep: React.FC<BasicsStepProps> = ({ character, updateCharacter, onNext }) => {
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const updateMeta = (field: string, value: string | number) => {
    updateCharacter({
      meta: {
        ...character.meta!,
        [field]: value
      }
    });
  };

  const selectedRace = RACES.find(r => r.name === character.meta?.race);
  const selectedSubrace = selectedRace?.subraces?.find(s => s.name === character.meta?.subrace);
  const selectedClass = CLASSES.find(c => c.name === character.meta?.class);
  const selectedBackground = BACKGROUNDS.find(b => b.name === character.meta?.background);

  const validateAndContinue = () => {
    const errors: string[] = [];
    
    if (!character.meta?.name?.trim()) errors.push('Character name is required');
    if (!character.meta?.race) errors.push('Race selection is required');
    if (!character.meta?.class) errors.push('Class selection is required');
    if (!character.meta?.level || character.meta.level < 1) errors.push('Valid level is required');
    
    setValidationErrors(errors);
    
    if (errors.length === 0) {
      onNext();
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Character Basics</h2>
        <p className="text-muted-foreground">
          Start by defining the core identity of your character. These choices will affect available options in later steps.
        </p>
      </div>

      {validationErrors.length > 0 && (
        <Card className="border-destructive bg-destructive/5">
          <CardContent className="pt-4">
            <div className="space-y-1">
              {validationErrors.map((error, index) => (
                <p key={index} className="text-destructive text-sm font-medium">• {error}</p>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Basic Info */}
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name" className="flex items-center gap-2">
              <User className="w-4 h-4" />
              Character Name *
            </Label>
            <Input
              id="name"
              placeholder="Enter character name"
              value={character.meta?.name || ''}
              onChange={(e) => updateMeta('name', e.target.value)}
              className="transition-smooth focus:shadow-glow"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="player">Player Name</Label>
            <Input
              id="player"
              placeholder="Enter player name"
              value={character.meta?.player || ''}
              onChange={(e) => updateMeta('player', e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="level">Level *</Label>
              <Input
                id="level"
                type="number"
                min="1"
                max="20"
                value={character.meta?.level || 1}
                onChange={(e) => updateMeta('level', parseInt(e.target.value) || 1)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="alignment">Alignment</Label>
              <Select value={character.meta?.alignment || ''} onValueChange={(value) => updateMeta('alignment', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select alignment" />
                </SelectTrigger>
                <SelectContent>
                  {['Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'True Neutral', 'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'].map(alignment => (
                    <SelectItem key={alignment} value={alignment}>
                      {alignment}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        {/* Race Selection */}
        <Card className="transition-smooth hover:shadow-magical">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Crown className="w-5 h-5 text-accent" />
              Race *
            </CardTitle>
            <CardDescription>
              Choose your character's ancestry and heritage
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Select value={character.meta?.race || ''} onValueChange={(value) => {
              updateMeta('race', value);
              // Clear subrace when race changes
              if (character.meta?.subrace) {
                updateMeta('subrace', '');
              }
            }}>
              <SelectTrigger>
                <SelectValue placeholder="Select race" />
              </SelectTrigger>
              <SelectContent>
                {RACES.map(race => (
                  <SelectItem key={race.name} value={race.name}>
                    {race.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Subrace Selection */}
            {selectedRace?.subraces && selectedRace.subraces.length > 0 && (
              <div className="mt-4">
                <Label className="text-sm font-medium mb-2 block">Subrace</Label>
                <Select value={character.meta?.subrace || ''} onValueChange={(value) => updateMeta('subrace', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select subrace" />
                  </SelectTrigger>
                  <SelectContent>
                    {selectedRace.subraces.map(subrace => (
                      <SelectItem key={subrace.name} value={subrace.name}>
                        {subrace.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {selectedRace && (
              <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                <h4 className="font-medium text-sm mb-2">
                  {selectedRace.name}
                  {selectedSubrace && ` (${selectedSubrace.name})`} Features
                </h4>
                <ul className="text-xs space-y-1 text-muted-foreground">
                  <li>• Speed: {selectedSubrace?.speed || selectedRace.speed} feet</li>
                  {(selectedSubrace?.darkvision || selectedRace.darkvision) && (
                    <li>• Darkvision: {selectedSubrace?.darkvision || selectedRace.darkvision} feet</li>
                  )}
                  <li>• Languages: {[...selectedRace.languages, ...(selectedSubrace?.additionalLanguages || [])].join(', ')}</li>
                  {selectedRace.features.slice(0, 2).map((feature, idx) => (
                    <li key={idx}>• {feature.name}</li>
                  ))}
                  {selectedSubrace?.features.slice(0, 2).map((feature, idx) => (
                    <li key={`sub-${idx}`}>• {feature.name}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Class Selection */}
        <Card className="transition-smooth hover:shadow-magical">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Briefcase className="w-5 h-5 text-primary" />
              Class *
            </CardTitle>
            <CardDescription>
              Your character's profession and combat role
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Select value={character.meta?.class || ''} onValueChange={(value) => updateMeta('class', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Select class" />
              </SelectTrigger>
              <SelectContent>
                {CLASSES.map(cls => (
                  <SelectItem key={cls.name} value={cls.name}>
                    {cls.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {selectedClass && (
              <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                <h4 className="font-medium text-sm mb-2">{selectedClass.name} Features</h4>
                <ul className="text-xs space-y-1 text-muted-foreground">
                  <li>• Hit Die: d{selectedClass.hitDie}</li>
                  <li>• Saving Throws: {selectedClass.savingThrows.join(', ')}</li>
                  <li>• Skills: Choose {selectedClass.skillChoices.choose} from {selectedClass.skillChoices.from.length} options</li>
                  {selectedClass.spellcasting && (
                    <li>• Spellcasting: {selectedClass.spellcasting.ability} ({selectedClass.spellcasting.progression})</li>
                  )}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Background Selection */}
        <Card className="transition-smooth hover:shadow-magical">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Briefcase className="w-5 h-5 text-secondary" />
              Background
            </CardTitle>
            <CardDescription>
              Your character's life before adventuring
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Select value={character.meta?.background || ''} onValueChange={(value) => updateMeta('background', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Select background" />
              </SelectTrigger>
              <SelectContent>
                {BACKGROUNDS.map(bg => (
                  <SelectItem key={bg.name} value={bg.name}>
                    {bg.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {selectedBackground && (
              <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                <h4 className="font-medium text-sm mb-2">{selectedBackground.name} Features</h4>
                <ul className="text-xs space-y-1 text-muted-foreground">
                  <li>• Skills: {selectedBackground.skills.join(', ')}</li>
                  {typeof selectedBackground.languages === 'number' && (
                    <li>• Languages: Choose {selectedBackground.languages}</li>
                  )}
                  <li>• Feature: {selectedBackground.feature.name}</li>
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end pt-6">
        <Button 
          onClick={validateAndContinue}
          className="bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Continue to Abilities
          <ChevronRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    </div>
  );
};