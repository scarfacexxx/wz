import random
from typing import Dict, Tuple, Optional
from .character import Character

class Combat:
    def __init__(self, player1: Character, player2: Character, bet_amount: float = 0):
        self.player1 = player1
        self.player2 = player2
        self.bet_amount = bet_amount
        self.turn = player1.twitter_handle
        self.hp1 = self._calculate_starting_hp(player1)
        self.hp2 = self._calculate_starting_hp(player2)
        self.combo_history = {player1.twitter_handle: [], player2.twitter_handle: []}
        self.status = 'active'
        self.effects = {player1.twitter_handle: {}, player2.twitter_handle: {}}
        
    def _calculate_starting_hp(self, player: Character) -> int:
        """Calculate starting HP including house bonuses."""
        base_hp = 100 + ((player.level - 1) * 10)
        if player.house == 'Gryffindor':
            base_hp += 5
        return base_hp
        
    def cast_spell(self, caster_handle: str, spell_name: str) -> Dict:
        """Process a spell cast and return the results."""
        if self.turn != caster_handle or self.status != 'active':
            return {'error': 'Not your turn or duel is over'}
            
        caster = self.player1 if caster_handle == self.player1.twitter_handle else self.player2
        target = self.player2 if caster_handle == self.player1.twitter_handle else self.player1
        
        if spell_name not in caster.spells:
            return {'error': 'You don\'t know this spell'}
            
        spell = caster.spells[spell_name]
        result = self._process_spell(caster, target, spell_name, spell)
        
        # Update combo history
        self.combo_history[caster_handle].append(spell_name)
        if len(self.combo_history[caster_handle]) > 3:
            self.combo_history[caster_handle].pop(0)
            
        # Switch turns
        self.turn = target.twitter_handle
        
        # Check for victory
        if self.hp1 <= 0:
            self.status = 'player2_wins'
            self._handle_duel_end(self.player2, self.player1)
        elif self.hp2 <= 0:
            self.status = 'player1_wins'
            self._handle_duel_end(self.player1, self.player2)
            
        return result
        
    def _process_spell(self, caster: Character, target: Character, spell_name: str, spell: Dict) -> Dict:
        """Process spell effects and calculate damage."""
        result = {'spell': spell_name, 'effects': []}
        
        # Check for Protego
        if spell.get('block'):
            self.effects[caster.twitter_handle]['protected'] = True
            if spell.get('heal'):
                heal = spell['heal']
                if caster == self.player1:
                    self.hp1 = min(self._calculate_starting_hp(caster), self.hp1 + heal)
                else:
                    self.hp2 = min(self._calculate_starting_hp(caster), self.hp2 + heal)
                result['effects'].append(f'Healed {heal} HP')
            return result
            
        # Calculate accuracy
        base_accuracy = spell.get('accuracy', 100)
        if caster.house == 'Ravenclaw':
            base_accuracy += 10
            
        # Calculate damage
        if spell.get('damage'):
            damage = random.randint(*spell['damage'])
            
            # Apply combo bonuses
            combo_bonus = self._calculate_combo_bonus(caster.twitter_handle)
            if combo_bonus > 0:
                damage = int(damage * (1 + combo_bonus))
                
            # Apply critical hits for Slytherin
            if caster.house == 'Slytherin' and random.random() < 0.2:  # 20% crit chance
                damage += 1
                result['effects'].append('Critical Hit!')
                
            # Apply damage
            if target == self.player1:
                if not self.effects.get(target.twitter_handle, {}).get('protected'):
                    self.hp1 -= damage
                    result['damage'] = damage
                else:
                    result['effects'].append('Attack Blocked!')
            else:
                if not self.effects.get(target.twitter_handle, {}).get('protected'):
                    self.hp2 -= damage
                    result['damage'] = damage
                else:
                    result['effects'].append('Attack Blocked!')
                    
        # Apply spell effects
        if spell.get('effect'):
            for effect, chance in spell['effect'].items():
                if random.random() * 100 < chance:
                    self.effects[target.twitter_handle][effect] = 2  # Effect lasts 2 turns
                    result['effects'].append(f'Applied {effect}')
                    
        # Clear protection after use
        self.effects[target.twitter_handle]['protected'] = False
        
        return result
        
    def _calculate_combo_bonus(self, player_handle: str) -> float:
        """Calculate damage bonus from spell combos."""
        combo_length = len(self.combo_history[player_handle])
        if combo_length == 2:
            return 0.10  # 10% bonus for 2-spell combo
        elif combo_length == 3:
            return 0.15  # 15% bonus for 3-spell combo
        return 0
        
    def _handle_duel_end(self, winner: Character, loser: Character) -> None:
        """Handle end of duel rewards and penalties."""
        winner.wins += 1
        winner.xp += 20
        if self.bet_amount > 0:
            winner.withdrawable_galleons += self.bet_amount * 2
            
        loser.losses += 1
        loser.xp += 10
        
    def to_dict(self) -> Dict:
        """Convert duel state to dictionary for database storage."""
        return {
            'player1': self.player1.twitter_handle,
            'player2': self.player2.twitter_handle,
            'bet_amount': self.bet_amount,
            'status': self.status,
            'turn': self.turn,
            'hp1': self.hp1,
            'hp2': self.hp2,
            'combo_history': self.combo_history,
            'effects': self.effects
        } 