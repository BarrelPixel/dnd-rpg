"""
Core data models for D&D RPG game
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Abilities:
    """Character abilities scores and modifiers"""
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def get_modifier(self, ability: str) -> int:
        """Calculate ability modifier"""
        score = getattr(self, ability.lower())
        return (score - 10) // 2

@dataclass
class Character:
    """Player character data"""
    name: str
    race: str
    character_class: str
    level: int = 1
    abilities: Abilities = field(default_factory=Abilities)
    max_hp: int = 10
    current_hp: int = 10
    armor_class: int = 10
    initiative_bonus: int = 0
    experience: int = 0
    inventory: Dict[str, int] = field(default_factory=dict)
    spells: Optional[List[str]] = None

    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.current_hp > 0

    def take_damage(self, amount: int) -> int:
        """Take damage and return actual damage dealt"""
        old_hp = self.current_hp
        self.current_hp = max(0, self.current_hp - amount)
        return old_hp - self.current_hp

    def heal(self, amount: int) -> int:
        """Heal and return actual healing done"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

@dataclass
class GameState:
    """Global game state"""
    character: Optional[Character] = None
    current_room: Optional[Dict] = None
    game_started: bool = False
    
    def is_game_active(self) -> bool:
        """Check if game is currently active"""
        return self.game_started and self.character is not None