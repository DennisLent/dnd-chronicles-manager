import React, { useState, useEffect } from 'react';
import { Sword, User, Backpack, Sparkles, Eye, FileText } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Character } from '@/types/character';
import { WizardNavigation } from './WizardNavigation';
import { CharacterSidebar } from './CharacterSidebar';
import { BasicsStep } from './steps/BasicsStep';
import { AbilitiesStep } from './steps/AbilitiesStep';
import { EquipmentStep } from './steps/EquipmentStep';
import { SpellsStep } from './steps/SpellsStep';
import { DetailsStep } from './steps/DetailsStep';
import { ReviewStep } from './steps/ReviewStep';

const WIZARD_STEPS = [
  { id: 'basics', label: 'Basics', icon: User },
  { id: 'abilities', label: 'Abilities', icon: Sword },
  { id: 'equipment', label: 'Equipment', icon: Backpack },
  { id: 'spells', label: 'Spells', icon: Sparkles },
  { id: 'details', label: 'Details', icon: FileText },
  { id: 'review', label: 'Review', icon: Eye }
] as const;

export type WizardStepId = typeof WIZARD_STEPS[number]['id'];

const CharacterCreator: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<WizardStepId>('basics');
  const [character, setCharacter] = useState<Partial<Character>>({
    meta: {
      name: '',
      player: '',
      race: '',
      class: '',
      level: 1,
      background: '',
      alignment: ''
    },
    schemaVersion: 1
  });

  // Auto-save to localStorage
  useEffect(() => {
    const saveTimer = setTimeout(() => {
      localStorage.setItem('dnd_character_draft', JSON.stringify(character));
    }, 500);

    return () => clearTimeout(saveTimer);
  }, [character]);

  // Load draft on mount
  useEffect(() => {
    const draft = localStorage.getItem('dnd_character_draft');
    if (draft) {
      try {
        const parsedDraft = JSON.parse(draft);
        setCharacter(parsedDraft);
      } catch (error) {
        console.warn('Failed to load character draft:', error);
      }
    }
  }, []);

  const updateCharacter = (updates: Partial<Character>) => {
    setCharacter(prev => ({
      ...prev,
      ...updates
    }));
  };

  const renderStep = () => {
    switch (currentStep) {
      case 'basics':
        return (
          <BasicsStep 
            character={character} 
            updateCharacter={updateCharacter}
            onNext={() => setCurrentStep('abilities')}
          />
        );
      case 'abilities':
        return (
          <AbilitiesStep 
            character={character} 
            updateCharacter={updateCharacter}
            onNext={() => setCurrentStep('equipment')}
            onPrevious={() => setCurrentStep('basics')}
          />
        );
      case 'equipment':
        return (
          <EquipmentStep 
            character={character} 
            updateCharacter={updateCharacter}
            onNext={() => setCurrentStep('spells')}
            onPrevious={() => setCurrentStep('abilities')}
          />
        );
      case 'spells':
        return (
          <SpellsStep 
            character={character} 
            updateCharacter={updateCharacter}
            onNext={() => setCurrentStep('details')}
            onPrevious={() => setCurrentStep('equipment')}
          />
        );
      case 'details':
        return (
          <DetailsStep
            character={character}
            updateCharacter={updateCharacter}
            onNext={() => setCurrentStep('review')}
            onPrevious={() => setCurrentStep('spells')}
          />
        );
      case 'review':
        return (
          <ReviewStep 
            character={character} 
            updateCharacter={updateCharacter}
            onPrevious={() => setCurrentStep('spells')}
          />
        );
      default:
        return (
          <div className="flex flex-col items-center justify-center h-96 text-muted-foreground">
            <div className="text-6xl mb-4">🔮</div>
            <h3 className="text-xl font-semibold mb-2">Step Coming Soon</h3>
            <p>The {WIZARD_STEPS.find(s => s.id === currentStep)?.label} step is being crafted with magical precision...</p>
          </div>
        );
    }
  };

  //const currentStepIndex = WIZARD_STEPS.findIndex(step => step.id === currentStep);

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <div className="flex w-full max-w-7xl mx-auto">
        {/* Sidebar */}
        <div className="w-80 flex-shrink-0">
          <CharacterSidebar character={character} />
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
                D&D 5e Character Creator
              </h1>
              <p className="text-muted-foreground">
                Create your perfect adventurer with guided steps and automatic validation
              </p>
            </div>

            {/* Wizard Navigation */}
            <WizardNavigation
              steps={WIZARD_STEPS}
              currentStep={currentStep}
              onStepClick={setCurrentStep}
              character={character}
            />

            {/* Step Content */}
            <Card className="mt-6 p-6 shadow-magical border-0 bg-card/80 backdrop-blur-sm">
              {renderStep()}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CharacterCreator;
