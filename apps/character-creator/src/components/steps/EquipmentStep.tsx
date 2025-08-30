import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Character } from '@/types/character';
import { CLASSES } from '@/data/staticRules';
import { Package, CheckCircle } from 'lucide-react';

interface EquipmentStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onNext: () => void;
  onPrevious: () => void;
}

export const EquipmentStep: React.FC<EquipmentStepProps> = ({
  character,
  updateCharacter,
  onNext,
  onPrevious
}) => {
  const classData = CLASSES.find(c => c.name === character.meta?.class);
  const equipmentChoices = character.classBlock?.chosenEquipment || {};
  const inventory = character.inventory || [];
  const backgroundEquipment = character.backgroundBlock?.equipment || [];

  const handleEquipmentChoice = (choiceIndex: number, option: string) => {
    const newChoices = { ...equipmentChoices, [choiceIndex]: option };
    updateCharacter({
      classBlock: {
        ...character.classBlock!,
        chosenEquipment: newChoices
      }
    });
  };

  const handleInventoryChange = (value: string) => {
    const items = value.split('\n').filter(item => item.trim());
    updateCharacter({ inventory: items });
  };

  const isValid = () => {
    if (!classData) return false;
    // Check that all equipment choices are made
    return classData.equipmentChoices.every((_, index) => 
      equipmentChoices[index] !== undefined
    );
  };

  const allEquipmentSelected = classData?.equipmentChoices.length === Object.keys(equipmentChoices).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Package className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-2xl font-bold">Starting Equipment</h2>
        </div>
        <p className="text-muted-foreground">
          Choose your starting equipment based on your class. Background equipment is added automatically.
        </p>
      </div>

      {/* Validation Status */}
      {!isValid() && (
        <Card className="p-4 border-warning bg-warning/5">
          <div className="flex items-center text-warning">
            <Package className="w-4 h-4 mr-2" />
            <span className="text-sm font-medium">
              Please select equipment for all {classData?.equipmentChoices.length || 0} choices
            </span>
          </div>
        </Card>
      )}

      {/* Class Equipment Choices */}
      {classData && (
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <h3 className="text-lg font-semibold">Class Equipment Choices</h3>
            <Badge variant="outline" className="ml-2">
              {Object.keys(equipmentChoices).length} / {classData.equipmentChoices.length}
            </Badge>
          </div>
          
          <div className="space-y-6">
            {classData.equipmentChoices.map((choice, index) => (
              <div key={index} className="space-y-3">
                <Label className="text-sm font-medium">
                  Choice {index + 1}: Select one option
                  {equipmentChoices[index] && (
                    <CheckCircle className="inline w-4 h-4 ml-2 text-success" />
                  )}
                </Label>
                <RadioGroup
                  value={equipmentChoices[index] || ''}
                  onValueChange={(value) => handleEquipmentChoice(index, value)}
                >
                  {choice.options.map((option, optionIndex) => (
                    <div key={optionIndex} className="flex items-center space-x-2">
                      <RadioGroupItem value={option} id={`choice-${index}-${optionIndex}`} />
                      <Label 
                        htmlFor={`choice-${index}-${optionIndex}`}
                        className="text-sm cursor-pointer"
                      >
                        {option}
                      </Label>
                    </div>
                  ))}
                </RadioGroup>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Background Equipment */}
      {backgroundEquipment.length > 0 && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Background Equipment</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {backgroundEquipment.map((item, index) => (
              <div key={index} className="flex items-center">
                <Badge variant="secondary" className="text-xs">
                  {item}
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Additional Inventory */}
      <Card className="p-6">
        <div className="space-y-4">
          <Label htmlFor="inventory">Additional Inventory (one item per line)</Label>
          <Textarea
            id="inventory"
            placeholder="Enter additional items, one per line..."
            value={inventory.join('\n')}
            onChange={(e) => handleInventoryChange(e.target.value)}
            className="min-h-24"
          />
          <p className="text-xs text-muted-foreground">
            Add any extra equipment, treasure, or personal items your character possesses.
          </p>
        </div>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onPrevious}>
          Previous: Abilities
        </Button>
        <Button 
          onClick={onNext} 
          disabled={!isValid()}
          className="bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Next: Spells
          {allEquipmentSelected && <CheckCircle className="w-4 h-4 ml-2" />}
        </Button>
      </div>
    </div>
  );
};