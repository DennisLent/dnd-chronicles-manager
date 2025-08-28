import React from 'react';
import { LucideIcon } from 'lucide-react';
import { Character } from '@/types/character';
import { WizardStepId } from './CharacterCreator';

interface WizardStep {
  id: WizardStepId;
  label: string;
  icon: LucideIcon;
}

interface WizardNavigationProps {
  steps: readonly WizardStep[];
  currentStep: WizardStepId;
  onStepClick: (stepId: WizardStepId) => void;
  character: Partial<Character>;
}

export const WizardNavigation: React.FC<WizardNavigationProps> = ({
  steps,
  currentStep,
  onStepClick,
  character
}) => {

  void character;
  
  const getStepStatus = (stepId: WizardStepId): 'active' | 'completed' | 'pending' => {
    if (stepId === currentStep) return 'active';
    
    // Simple completion logic - can be enhanced with real validation
    const currentIndex = steps.findIndex(s => s.id === currentStep);
    const stepIndex = steps.findIndex(s => s.id === stepId);
    
    if (stepIndex < currentIndex) return 'completed';
    return 'pending';
  };

  return (
    <div className="flex items-center justify-between w-full bg-card/50 backdrop-blur-sm border border-border rounded-lg p-4 shadow-soft">
      {steps.map((step, index) => {
        const status = getStepStatus(step.id);
        const Icon = step.icon;
        
        return (
          <React.Fragment key={step.id}>
            <button
              onClick={() => onStepClick(step.id)}
              className="group flex flex-col items-center space-y-2 transition-magical hover:scale-105"
              disabled={status === 'pending' && step.id !== currentStep}
            >
              <div className={`step-indicator ${status}`}>
                <Icon className="w-4 h-4" />
              </div>
              <span className={`text-xs font-medium transition-colors ${
                status === 'active' 
                  ? 'text-primary' 
                  : status === 'completed' 
                  ? 'text-primary/80' 
                  : 'text-muted-foreground'
              }`}>
                {step.label}
              </span>
            </button>
            
            {index < steps.length - 1 && (
              <div className={`flex-1 h-px transition-colors mx-4 ${
                getStepStatus(steps[index + 1].id) === 'completed' 
                  ? 'bg-primary/30' 
                  : 'bg-border'
              }`} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};