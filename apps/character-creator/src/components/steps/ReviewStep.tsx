import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Character } from '@/types/character';
import { Eye, Download, AlertTriangle, CheckCircle } from 'lucide-react';

interface ReviewStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onPrevious: () => void;
}

export const ReviewStep: React.FC<ReviewStepProps> = ({
  character,
  updateCharacter,
  onPrevious
}) => {
  // const level = character.meta?.level || 1;
  // const proficiencyBonus = PROFICIENCY_BONUS[level] || 2;
  void updateCharacter;
  
  // Calculate ability modifiers
  const getAbilityMod = (score: number) => Math.floor((score - 10) / 2);
  const formatMod = (mod: number) => mod >= 0 ? `+${mod}` : `${mod}`;

  // Validation
  const getValidationErrors = () => {
    const errors = [];
    
    if (!character.meta?.name) errors.push('Character name is required');
    if (!character.meta?.race) errors.push('Race selection is required');
    if (!character.meta?.class) errors.push('Class selection is required');
    if (!character.baseAbilities) errors.push('Ability scores must be set');
    
    return errors;
  };

  const validationErrors = getValidationErrors();
  const isValid = validationErrors.length === 0;

  const exportCharacter = () => {
    const characterData = {
      ...character,
      exportedAt: new Date().toISOString(),
      schemaVersion: 1
    };
    
    const dataStr = JSON.stringify(characterData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${character.meta?.name || 'character'}_character.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Eye className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-2xl font-bold">Character Review</h2>
        </div>
        <p className="text-muted-foreground">
          Review your character details before exporting. Make sure everything looks correct.
        </p>
      </div>

      {/* Validation Status */}
      <Card className={`p-4 ${isValid ? 'border-success bg-success/5' : 'border-warning bg-warning/5'}`}>
        <div className={`flex items-center ${isValid ? 'text-success' : 'text-warning'}`}>
          {isValid ? (
            <CheckCircle className="w-5 h-5 mr-2" />
          ) : (
            <AlertTriangle className="w-5 h-5 mr-2" />
          )}
          <span className="font-medium">
            {isValid ? 'Character is ready for export!' : `${validationErrors.length} validation errors`}
          </span>
        </div>
        {!isValid && (
          <ul className="mt-2 text-sm space-y-1">
            {validationErrors.map((error, index) => (
              <li key={index} className="ml-7">• {error}</li>
            ))}
          </ul>
        )}
      </Card>

      {/* Character Meta */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Character Information</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm text-muted-foreground">Name:</span>
            <div className="font-medium">{character.meta?.name || 'Unnamed Character'}</div>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Player:</span>
            <div className="font-medium">{character.meta?.player || 'No player set'}</div>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Race:</span>
            <div className="font-medium">
              {character.meta?.race}
              {character.meta?.subrace && ` (${character.meta.subrace})`}
            </div>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Class:</span>
            <div className="font-medium">{character.meta?.class}</div>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Background:</span>
            <div className="font-medium">{character.meta?.background}</div>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Level:</span>
            <div className="font-medium">{character.meta?.level}</div>
          </div>
        </div>
      </Card>

      {/* Abilities */}
      {character.abilities && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Final Ability Scores</h3>
          <div className="grid grid-cols-3 gap-4">
            {Object.entries(character.abilities).map(([ability, score]) => (
              <div key={ability} className="text-center">
                <div className="text-sm text-muted-foreground capitalize">{ability}</div>
                <div className="text-xl font-bold">{score}</div>
                <div className="text-sm text-muted-foreground">
                  {formatMod(getAbilityMod(score))}
                </div>
              </div>
            ))}
          </div>
          
          {character.baseAbilities && (
            <div className="mt-4 pt-4 border-t">
              <div className="text-sm text-muted-foreground mb-2">Base Scores (before racial bonuses):</div>
              <div className="grid grid-cols-6 gap-2 text-xs">
                {Object.entries(character.baseAbilities).map(([ability, score]) => (
                  <div key={ability} className="text-center">
                    <div className="capitalize">{ability.slice(0, 3)}</div>
                    <div>{score}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Card>
      )}

      {/* Combat Stats */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Combat Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-sm text-muted-foreground">Hit Points</div>
            <div className="text-xl font-bold">{character.hp?.max || 0}</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-muted-foreground">Armor Class</div>
            <div className="text-xl font-bold">{character.ac || 10}</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-muted-foreground">Initiative</div>
            <div className="text-xl font-bold">
              {character.abilities ? formatMod(getAbilityMod(character.abilities.dexterity)) : '+0'}
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-muted-foreground">Speed</div>
            <div className="text-xl font-bold">{character.speed || 30} ft</div>
          </div>
        </div>
      </Card>

      {/* Skills */}
      {character.skills && Object.keys(character.skills).length > 0 && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Skills</h3>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(character.skills).map(([skill, bonus]) => (
              <div key={skill} className="flex justify-between">
                <span className="capitalize">{skill}</span>
                <span className="font-medium">{formatMod(bonus)}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Equipment */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Equipment</h3>
        
        {/* Class Equipment */}
        {character.classBlock?.chosenEquipment && (
          <div className="mb-4">
            <h4 className="font-medium mb-2">Class Equipment</h4>
            <div className="space-y-1">
              {Object.values(character.classBlock.chosenEquipment).map((item, index) => (
                <Badge key={index} variant="secondary" className="mr-2 mb-1">
                  {item}
                </Badge>
              ))}
            </div>
          </div>
        )}
        
        {/* Background Equipment */}
        {character.backgroundBlock?.equipment && character.backgroundBlock.equipment.length > 0 && (
          <div className="mb-4">
            <h4 className="font-medium mb-2">Background Equipment</h4>
            <div className="space-y-1">
              {character.backgroundBlock.equipment.map((item, index) => (
                <Badge key={index} variant="outline" className="mr-2 mb-1">
                  {item}
                </Badge>
              ))}
            </div>
          </div>
        )}
        
        {/* Additional Inventory */}
        {character.inventory && character.inventory.length > 0 && (
          <div>
            <h4 className="font-medium mb-2">Additional Items</h4>
            <div className="space-y-1">
              {character.inventory.map((item, index) => (
                <Badge key={index} variant="default" className="mr-2 mb-1">
                  {item}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* Spells */}
      {character.spells && character.spells.chosenSpells.length > 0 && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Spells</h3>
          <div className="mb-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-sm text-muted-foreground">Save DC</div>
              <div className="font-bold">{character.spells.saveDC}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Attack Bonus</div>
              <div className="font-bold">+{character.spells.attackBonus}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Casting Ability</div>
              <div className="font-bold capitalize">{character.spells.castingAbility}</div>
            </div>
          </div>
          <Separator className="my-4" />
          <div className="space-y-3">
            {character.spells.chosenSpells.map((spell, index) => (
              <div key={index} className="border rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="font-medium">{spell.name}</div>
                  <Badge variant="outline">
                    Level {spell.level} {spell.school}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground">{spell.description}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Navigation */}
      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onPrevious}>
          Previous: Spells
        </Button>
        <Button 
          onClick={exportCharacter}
          disabled={!isValid}
          className="bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Download className="w-4 h-4 mr-2" />
          Export Character
        </Button>
      </div>
    </div>
  );
};