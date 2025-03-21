import random
import json
from typing import Dict, List, Optional

class Character:
    HOUSES = ['Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff']
    HOUSE_BONUSES = {
        'Ravenclaw': {'accuracy': 10},  # +10% accuracy
        'Gryffindor': {'hp': 5},        # +5 HP
        'Slytherin': {'crit_dmg': 1},   # +1 crit damage
        'Hufflepuff': {'hp_regen': 1}   # +1 HP/turn
    }
    
    def __init__(self, twitter_handle: str, name: str):
        self.twitter_handle = twitter_handle
        self.name = name
        self.house = random.choice(self.HOUSES)
        self.level = 1
        self.xp = 0
        self.hp = 100
        self.bonus_galleons = 20.00
        self.withdrawable_galleons = 0.00
        self.spells = self._get_starting_spells()
        self.potions = {}
        self.wins = 0
        self.losses = 0
        self.titles = []
        
    def _get_starting_spells(self) -> Dict:
        return {
            'Incendio': {
                'damage': (3, 6),
                'accuracy': 110,
                'effect': {'burn': 20}
            },
            'Protego': {
                'block': True,
                'heal': 2
            }
        }
        
    def level_up(self) -> Dict:
        """Level up the character and return new abilities."""
        self.level += 1
        self.xp = self.xp - (100 * (self.level - 1))
        new_abilities = self._get_level_abilities(self.level)
        self.spells.update(new_abilities.get('spells', {}))
        return new_abilities
        
    def _get_level_abilities(self, level: int) -> Dict:
        """Get new abilities for the given level."""
        abilities = {
            2: {'spells': {'Flipendo': {'damage': (4, 7), 'accuracy': 100, 'effect': {'stun': 60}}}},
            3: {'spells': {'Reducto': {'damage': (5, 8), 'accuracy': 95, 'effect': {'armor_break': 30}}}},
            # Add more spells for other levels
        }
        return abilities.get(level, {'spells': {}})
        
    def to_dict(self) -> Dict:
        """Convert character to dictionary for database storage."""
        return {
            'twitter_handle': self.twitter_handle,
            'name': self.name,
            'house': self.house,
            'level': self.level,
            'xp': self.xp,
            'hp': self.hp,
            'bonus_galleons': self.bonus_galleons,
            'withdrawable_galleons': self.withdrawable_galleons,
            'spells': json.dumps(self.spells),
            'potions': json.dumps(self.potions),
            'wins': self.wins,
            'losses': self.losses,
            'titles': json.dumps(self.titles)
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """Create character from dictionary (database record)."""
        char = cls(data['twitter_handle'], data['name'])
        char.house = data['house']
        char.level = data['level']
        char.xp = data['xp']
        char.hp = data['hp']
        char.bonus_galleons = float(data['bonus_galleons'])
        char.withdrawable_galleons = float(data['withdrawable_galleons'])
        char.spells = json.loads(data['spells'])
        char.potions = json.loads(data['potions'])
        char.wins = data['wins']
        char.losses = data['losses']
        char.titles = json.loads(data['titles'])
        return char 