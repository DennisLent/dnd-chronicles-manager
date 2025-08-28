import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Dices, Target, Edit3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Character, Abilities, AbilityGenerationMethod } from '@/types/character';
import { POINT_BUY_COSTS, STANDARD_ARRAY, ABILITIES } from '@/data/staticRules';

interface AbilitiesStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onNext: () => void;
  onPrevious: () => void;
}

export const AbilitiesStep: React.FC<AbilitiesStepProps> = ({ 
  character, 
  updateCharacter, 
  onNext, 
  onPrevious 
}) => {
  const [method, setMethod] = useState<AbilityGenerationMethod>('pointBuy');
  const [pointsRemaining, setPointsRemaining] = useState(27);
  const [standardArrayAssigned, setStandardArrayAssigned] = useState<{ [value: number]: keyof Abilities | null }>({
    15: null, 14: null, 13: null, 12: null, 10: null, 8: null
  });
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const baseAbilities = character.baseAbilities || {
    strength: 8, dexterity: 8, constitution: 8, intelligence: 8, wisdom: 8, charisma: 8
  };

  const getAbilityModifier = (score: number) => Math.floor((score - 10) / 2);

  // Point Buy Methods
  const calculatePointsUsed = (abilities: Abilities) => {
    return Object.values(abilities).reduce((total, score) => {
      return total + (POINT_BUY_COSTS[score] || 0);
    }, 0);
  };

  const canIncreaseAbility = (ability: keyof Abilities) => {
    const currentScore = baseAbilities[ability];
    if (currentScore >= 15) return false;
    
    const newCost = POINT_BUY_COSTS[currentScore + 1] || 0;
    const currentCost = POINT_BUY_COSTS[currentScore] || 0;
    const costDiff = newCost - currentCost;
    
    return pointsRemaining >= costDiff;
  };

  const canDecreaseAbility = (ability: keyof Abilities) => {
    return baseAbilities[ability] > 8;
  };

  const adjustAbility = (ability: keyof Abilities, delta: number) => {
    const currentScore = baseAbilities[ability];
    const newScore = Math.max(8, Math.min(15, currentScore + delta));
    
    if (newScore === currentScore) return;
    
    const newAbilities = { ...baseAbilities, [ability]: newScore };
    const newPointsUsed = calculatePointsUsed(newAbilities);
    
    if (newPointsUsed <= 27) {
      updateCharacter({ baseAbilities: newAbilities });
      setPointsRemaining(27 - newPointsUsed);
    }
  };

  // Standard Array Methods
  const assignStandardArrayValue = (value: number, ability: keyof Abilities) => {
    const newAssignment = { ...standardArrayAssigned };
    
    // Clear previous assignment of this ability
    Object.keys(newAssignment).forEach(key => {
      if (newAssignment[parseInt(key)] === ability) {
        newAssignment[parseInt(key)] = null;
      }
    });
    
    // Clear previous assignment of this value
    if (newAssignment[value]) {
      newAssignment[value] = null;
    }
    
    // Make new assignment
    newAssignment[value] = ability;
    setStandardArrayAssigned(newAssignment);
    
    // Update character abilities
    const newAbilities = { ...baseAbilities };
    Object.entries(newAssignment).forEach(([val, abil]) => {
      if (abil) {
        newAbilities[abil] = parseInt(val);
      } else {
        // Reset unassigned abilities to 8
        ABILITIES.forEach(ab => {
          if (!Object.values(newAssignment).includes(ab)) {
            newAbilities[ab] = 8;
          }
        });
      }
    });
    
    updateCharacter({ baseAbilities: newAbilities });
  };

  // Manual entry
  const setManualAbility = (ability: keyof Abilities, value: string) => {
    const score = parseInt(value) || 8;
    const clampedScore = Math.max(1, Math.min(20, score));
    
    updateCharacter({
      baseAbilities: { ...baseAbilities, [ability]: clampedScore }
    });
  };

  // Validation
  const validateAndContinue = () => {
    const errors: string[] = [];
    
    if (method === 'pointBuy' && pointsRemaining !== 0) {
      errors.push(`You have ${pointsRemaining} points remaining. Spend all points to continue.`);
    }
    
    if (method === 'standardArray') {
      const assigned = Object.values(standardArrayAssigned).filter(v => v !== null).length;
      if (assigned !== 6) {
        errors.push(`You must assign all 6 standard array values. Currently assigned: ${assigned}/6`);
      }
    }
    
    setValidationErrors(errors);
    
    if (errors.length === 0) {
      onNext();
    }
  };

  // Initialize points remaining on method change
  useEffect(() => {
    if (method === 'pointBuy') {
      const used = calculatePointsUsed(baseAbilities);
      setPointsRemaining(27 - used);
    }
  }, [method, baseAbilities]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Ability Scores</h2>
        <p className="text-muted-foreground">
          Determine your character's raw abilities using one of three methods. These will be modified by your race later.
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

      <Tabs value={method} onValueChange={(value) => setMethod(value as AbilityGenerationMethod)}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="pointBuy" className="flex items-center gap-2">
            <Target className="w-4 h-4" />
            Point Buy
          </TabsTrigger>
          <TabsTrigger value="standardArray" className="flex items-center gap-2">
            <Dices className="w-4 h-4" />
            Standard Array
          </TabsTrigger>
          <TabsTrigger value="manual" className="flex items-center gap-2">
            <Edit3 className="w-4 h-4" />
            Manual Entry
          </TabsTrigger>
        </TabsList>

        <TabsContent value="pointBuy" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Point Buy System
                <Badge variant="outline" className="bg-primary text-primary-foreground text-sm px-1.5 py-1.5 rounded-md shadow-soft">
                  Points Remaining: {pointsRemaining}
                </Badge>
              </CardTitle>
              <CardDescription>
                Spend 27 points to customize your abilities. Each score starts at 8 and can go up to 15.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {ABILITIES.map((ability) => {
                  const score = baseAbilities[ability];
                  const modifier = getAbilityModifier(score);
                  
                  return (
                    <div key={ability} className="stat-display">
                      <Label className="stat-label capitalize">
                        {ability}
                      </Label>
                      
                      <div className="flex items-center gap-2 mt-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => adjustAbility(ability, -1)}
                          disabled={!canDecreaseAbility(ability)}
                          className="w-8 h-8 p-0"
                        >
                          -
                        </Button>
                        
                        <div className="text-center min-w-[3rem]">
                          <div className="stat-value text-lg">{score}</div>
                          <div className="stat-modifier">
                            {modifier >= 0 ? '+' : ''}{modifier}
                          </div>
                        </div>
                        
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => adjustAbility(ability, 1)}
                          disabled={!canIncreaseAbility(ability)}
                          className="w-8 h-8 p-0"
                        >
                          +
                        </Button>
                      </div>
                      
                      <div className="text-xs text-muted-foreground mt-1">
                        Cost: {POINT_BUY_COSTS[score]}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="standardArray" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Standard Array</CardTitle>
              <CardDescription>
                Assign these predetermined values: 15, 14, 13, 12, 10, 8 to your abilities.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {STANDARD_ARRAY.map(value => (
                    <Badge 
                      key={value} 
                      variant={standardArrayAssigned[value] ? "default" : "secondary"}
                      className="text-sm px-3 py-1"
                    >
                      {value} {standardArrayAssigned[value] && `→ ${standardArrayAssigned[value]}`}
                    </Badge>
                  ))}
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {ABILITIES.map((ability) => {
                    const score = baseAbilities[ability];
                    const modifier = getAbilityModifier(score);
                    const assignedValue = Object.entries(standardArrayAssigned)
                      .find(([_, assigned]) => assigned === ability)?.[0];
                    
                    return (
                      <div key={ability} className="stat-display">
                        <Label className="stat-label capitalize">
                          {ability}
                        </Label>
                        
                        <div className="stat-value">{score}</div>
                        <div className="stat-modifier">
                          {modifier >= 0 ? '+' : ''}{modifier}
                        </div>
                        
                        <select
                          value={assignedValue || ''}
                          onChange={(e) => {
                            const value = parseInt(e.target.value);
                            if (value) {
                              assignStandardArrayValue(value, ability);
                            }
                          }}
                          className="mt-2 text-xs bg-background border border-border rounded px-2 py-1"
                        >
                          <option value="">Assign...</option>
                          {STANDARD_ARRAY.map(value => (
                            <option 
                              key={value} 
                              value={value}
                              disabled={!standardArrayAssigned[value] && standardArrayAssigned[value] !== ability}
                            >
                              {value}
                            </option>
                          ))}
                        </select>
                      </div>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="manual" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Manual Entry</CardTitle>
              <CardDescription>
                Enter ability scores directly (1-20). Values outside the normal range (8-15) will be highlighted.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {ABILITIES.map((ability) => {
                  const score = baseAbilities[ability];
                  const modifier = getAbilityModifier(score);
                  const isOutOfRange = score < 8 || score > 15;
                  
                  return (
                    <div key={ability} className="stat-display">
                      <Label className="stat-label capitalize">
                        {ability}
                      </Label>
                      
                      <Input
                        type="number"
                        min="1"
                        max="20"
                        value={score}
                        onChange={(e) => setManualAbility(ability, e.target.value)}
                        className={`text-center text-lg font-bold mt-2 ${
                          isOutOfRange ? 'border-amber-500 bg-amber-50' : ''
                        }`}
                      />
                      
                      <div className="stat-modifier">
                        {modifier >= 0 ? '+' : ''}{modifier}
                      </div>
                      
                      {isOutOfRange && (
                        <div className="text-xs text-amber-600 mt-1">
                          Outside normal range
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onPrevious}>
          <ChevronLeft className="w-4 h-4 mr-2" />
          Back to Basics
        </Button>
        
        <Button 
          onClick={validateAndContinue}
          className="bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Continue to Class
          <ChevronRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    </div>
  );
};