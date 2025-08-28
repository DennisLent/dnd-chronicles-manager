import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Character } from '@/types/character';
import { APPEARANCE_FIELDS, PERSONALITY_FIELDS } from '@/data/staticRules';

interface DetailsStepProps {
  character: Partial<Character>;
  updateCharacter: (updates: Partial<Character>) => void;
  onNext: () => void;
  onPrevious: () => void;
}

export const DetailsStep: React.FC<DetailsStepProps> = ({ character, updateCharacter, onNext, onPrevious }) => {
  const appearance = character.appearance || '';
  const personality = character.personality || '';
  const notes = character.notes || '';

  const handleChange = (field: 'appearance' | 'personality' | 'notes', value: string) => {
    updateCharacter({ [field]: value } as any);
  };

  const appearancePlaceholder = `Include details like: ${APPEARANCE_FIELDS.join(', ')}.`;
  const personalityPlaceholder = `Write about: ${PERSONALITY_FIELDS.join(', ')}.`;

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold">Character Details</h2>
        <p className="text-muted-foreground">Bring your character to life with appearance, personality, and backstory notes.</p>
      </div>

      <Card className="p-6">
        <div className="space-y-4">
          <div>
            <Label htmlFor="appearance">Appearance</Label>
            <Textarea
              id="appearance"
              value={appearance}
              onChange={(e) => handleChange('appearance', e.target.value)}
              placeholder={appearancePlaceholder}
              className="min-h-28"
            />
          </div>
          <div>
            <Label htmlFor="personality">Personality</Label>
            <Textarea
              id="personality"
              value={personality}
              onChange={(e) => handleChange('personality', e.target.value)}
              placeholder={personalityPlaceholder}
              className="min-h-28"
            />
          </div>
          <div>
            <Label htmlFor="notes">Notes / Backstory</Label>
            <Textarea
              id="notes"
              value={notes}
              onChange={(e) => handleChange('notes', e.target.value)}
              placeholder="Write anything else that makes this character your own (hooks, goals, allies, secrets)."
              className="min-h-28"
            />
          </div>
        </div>
      </Card>

      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onPrevious}>Previous: Spells</Button>
        <Button onClick={onNext}>Next: Review</Button>
      </div>
    </div>
  );
};

