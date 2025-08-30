import React from 'react';
import { Shield, Eye, Zap, MapPin } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Character } from '@/types/character';
import { PROFICIENCY_BONUS } from '@/data/staticRules';

interface CharacterSidebarProps {
  character: Partial<Character>;
}

export const CharacterSidebar: React.FC<CharacterSidebarProps> = ({ character }) => {
  // Calculate derived stats
  const getAbilityModifier = (score: number = 10) => Math.floor((score - 10) / 2);
  
  const dexMod = getAbilityModifier(character.abilities?.dexterity);
  const conMod = getAbilityModifier(character.abilities?.constitution);
  const wisMod = getAbilityModifier(character.abilities?.wisdom);
  
  const proficiencyBonus = character.meta?.level ? PROFICIENCY_BONUS[character.meta.level] : 2;
  
  const initiative = dexMod;
  const passivePerception = 10 + wisMod; // + proficiency if skilled
  const hitPoints = character.classBlock?.hitDie ? 
    Math.max(1, (character.classBlock.hitDie + conMod)) : 
    null;
  const speed = character.raceBlock?.speed || 30;
  const darkvision = character.raceBlock?.darkvision;

  const StatBlock: React.FC<{ 
    icon: React.ReactNode; 
    label: string; 
    value: string | number | null;
    modifier?: string;
  }> = ({ icon, label, value, modifier }) => (
    <div className="stat-display">
      <div className="flex items-center gap-2 mb-1">
        {icon}
        <span className="stat-label">{label}</span>
      </div>
      <div className="stat-value">
        {value ?? '—'}
      </div>
      {modifier && (
        <div className="stat-modifier">
          {modifier}
        </div>
      )}
    </div>
  );

  return (
    <div className="h-screen p-4 border-r border-border bg-card/30 backdrop-blur-sm sticky top-0">
      <Card className="shadow-soft border-0 bg-card/80 backdrop-blur-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg font-semibold bg-gradient-primary bg-clip-text text-transparent">
            Character Stats
          </CardTitle>
          {character.meta?.name && (
            <p className="text-sm text-muted-foreground">{character.meta.name}</p>
          )}
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Basic Info */}
          <div className="space-y-2">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Basic Info
            </div>
            <div className="text-sm space-y-1">
              <div><span className="font-medium">Race:</span> {character.meta?.race || '—'}</div>
              <div><span className="font-medium">Class:</span> {character.meta?.class || '—'}</div>
              <div><span className="font-medium">Level:</span> {character.meta?.level || 1}</div>
              <div><span className="font-medium">Background:</span> {character.meta?.background || '—'}</div>
            </div>
          </div>

          <Separator />

          {/* Combat Stats */}
          <div className="space-y-3">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Combat Stats
            </div>
            
            <StatBlock
              icon={<Zap className="w-4 h-4 text-accent" />}
              label="Initiative"
              value={initiative}
              modifier={initiative >= 0 ? `+${initiative}` : `${initiative}`}
            />
            
            <StatBlock
              icon={<Shield className="w-4 h-4 text-primary" />}
              label="Hit Points"
              value={hitPoints}
              modifier={character.meta?.level === 1 ? 'Level 1' : undefined}
            />
            
            <StatBlock
              icon={<Eye className="w-4 h-4 text-secondary" />}
              label="Passive Perception"
              value={passivePerception}
            />
            
            <StatBlock
              icon={<MapPin className="w-4 h-4 text-muted-foreground" />}
              label="Speed"
              value={speed}
              modifier="feet"
            />
            
            {darkvision && (
              <StatBlock
                icon={<Eye className="w-4 h-4 text-purple-500" />}
                label="Darkvision"
                value={darkvision}
                modifier="feet"
              />
            )}
          </div>

          <Separator />

          {/* Abilities */}
          <div className="space-y-3">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Abilities
            </div>
            
            <div className="grid grid-cols-2 gap-2 text-xs">
              {character.abilities && Object.entries(character.abilities).map(([ability, score]) => (
                <div key={ability} className="flex justify-between items-center">
                  <span className="font-medium capitalize">{ability.slice(0, 3)}</span>
                  <div className="text-right">
                    <div className="font-bold">{score}</div>
                    <div className="text-muted-foreground">
                      {getAbilityModifier(score) >= 0 ? '+' : ''}{getAbilityModifier(score)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Proficiency Bonus */}
          <div className="text-xs">
            <span className="font-medium text-muted-foreground">Proficiency Bonus: </span>
            <span className="font-bold text-primary">+{proficiencyBonus}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};