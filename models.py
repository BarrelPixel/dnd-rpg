"""
Data models for D&D 3.5e RPG
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class CharacterClass(Enum):
    FIGHTER = "Fighter"
    WIZARD = "Wizard"
    CLERIC = "Cleric"
    ROGUE = "Rogue"

class Race(Enum):
    HUMAN = "Human"
    ELF = "Elf"
    DWARF = "Dwarf"
    HALFLING = "Halfling"

class SpellSchool(Enum):
    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    TRANSMUTATION = "Transmutation"

class SpellEffect(Enum):
    HEAL = "heal"
    DAMAGE = "damage"
    BUFF = "buff"
    STATUS = "status"
    UTILITY = "utility"

@dataclass
class Abilities:
    """Character ability scores"""
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    
    def get_modifier(self, ability: str) -> int:
        """Calculate ability modifier"""
        score = getattr(self, ability.lower())
        return (score - 10) // 2
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary format for compatibility"""
        return {
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'charisma': self.charisma
        }

@dataclass
class Character:
    """Player character data"""
    name: str
    race: Race
    character_class: CharacterClass
    level: int = 1
    abilities: Abilities = field(default_factory=Abilities)
    max_hp: int = 0
    current_hp: int = 0
    armor_class: int = 10
    initiative_bonus: int = 0
    experience: int = 0
    inventory: Dict[str, int] = field(default_factory=dict)
    equipment: Dict[str, int] = field(default_factory=dict)
    spells: Optional[List[str]] = None
    feats: List[str] = field(default_factory=list)
    skills: Dict[str, int] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    class_features: List[str] = field(default_factory=list)
    
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for compatibility"""
        return {
            'name': self.name,
            'race': self.race.value,
            'class': self.character_class.value,
            'level': self.level,
            'abilities': self.abilities.to_dict(),
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'armor_class': self.armor_class,
            'initiative_bonus': self.initiative_bonus,
            'experience': self.experience,
            'inventory': self.inventory,
            'equipment': self.equipment,
            'spells': self.spells,
            'feats': self.feats,
            'skills': self.skills,
            'traits': self.traits,
            'class_features': self.class_features
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create Character from dictionary"""
        abilities = Abilities(**data['abilities'])
        return cls(
            name=data['name'],
            race=Race(data['race']),
            character_class=CharacterClass(data['class']),
            level=data['level'],
            abilities=abilities,
            max_hp=data['max_hp'],
            current_hp=data['current_hp'],
            armor_class=data['armor_class'],
            initiative_bonus=data['initiative_bonus'],
            experience=data['experience'],
            inventory=data.get('inventory', {}),
            equipment=data.get('equipment', {}),
            spells=data.get('spells'),
            feats=data.get('feats', []),
            skills=data.get('skills', {}),
            traits=data.get('traits', []),
            class_features=data.get('class_features', [])
        )

@dataclass
class Monster:
    """Monster data"""
    name: str
    level: int
    max_hp: int
    current_hp: int
    armor_class: int
    initiative_bonus: int
    attack_bonus: int
    damage: str
    damage_bonus: int
    xp_value: int
    description: str
    
    def is_alive(self) -> bool:
        """Check if monster is alive"""
        return self.current_hp > 0
    
    def take_damage(self, amount: int) -> int:
        """Take damage and return actual damage dealt"""
        old_hp = self.current_hp
        self.current_hp = max(0, self.current_hp - amount)
        return old_hp - self.current_hp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for compatibility"""
        return {
            'name': self.name,
            'level': self.level,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'armor_class': self.armor_class,
            'initiative_bonus': self.initiative_bonus,
            'attack_bonus': self.attack_bonus,
            'damage': self.damage,
            'damage_bonus': self.damage_bonus,
            'xp_value': self.xp_value,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Monster':
        """Create Monster from dictionary"""
        return cls(
            name=data['name'],
            level=data['level'],
            max_hp=data['max_hp'],
            current_hp=data.get('current_hp', data['max_hp']),
            armor_class=data['armor_class'],
            initiative_bonus=data['initiative_bonus'],
            attack_bonus=data['attack_bonus'],
            damage=data['damage'],
            damage_bonus=data['damage_bonus'],
            xp_value=data['xp_value'],
            description=data['description']
        )

@dataclass
class Spell:
    """Spell data"""
    name: str
    level: int
    school: SpellSchool
    subschool: str
    casting_time: str
    range: str
    target: str
    duration: str
    saving_throw: str
    spell_resistance: str
    description: str
    effect: SpellEffect
    character_class: CharacterClass
    
    # Effect-specific fields
    heal_amount: Optional[str] = None
    damage_amount: Optional[str] = None
    damage_type: Optional[str] = None
    buff_type: Optional[str] = None
    bonus: Optional[int] = None
    status_type: Optional[str] = None
    area_effect: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for compatibility"""
        return {
            'name': self.name,
            'level': self.level,
            'school': self.school.value,
            'subschool': self.subschool,
            'casting_time': self.casting_time,
            'range': self.range,
            'target': self.target,
            'duration': self.duration,
            'saving_throw': self.saving_throw,
            'spell_resistance': self.spell_resistance,
            'description': self.description,
            'effect': self.effect.value,
            'class': self.character_class.value,
            'heal_amount': self.heal_amount,
            'damage_amount': self.damage_amount,
            'damage_type': self.damage_type,
            'buff_type': self.buff_type,
            'bonus': self.bonus,
            'status_type': self.status_type,
            'area_effect': self.area_effect
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Spell':
        """Create Spell from dictionary"""
        return cls(
            name=data['name'],
            level=data['level'],
            school=SpellSchool(data['school']),
            subschool=data['subschool'],
            casting_time=data['casting_time'],
            range=data['range'],
            target=data['target'],
            duration=data['duration'],
            saving_throw=data['saving_throw'],
            spell_resistance=data['spell_resistance'],
            description=data['description'],
            effect=SpellEffect(data['effect']),
            character_class=CharacterClass(data['class']),
            heal_amount=data.get('heal_amount'),
            damage_amount=data.get('damage_amount'),
            damage_type=data.get('damage_type'),
            buff_type=data.get('buff_type'),
            bonus=data.get('bonus'),
            status_type=data.get('status_type'),
            area_effect=data.get('area_effect', False)
        )

@dataclass
class Room:
    """Dungeon room data"""
    room_type: str
    x: int
    y: int
    visited: bool = False
    exits: Dict[str, tuple] = field(default_factory=dict)
    encounter: Optional[List[Monster]] = None
    treasure: Optional[Dict[str, Any]] = None
    description: str = ""
    name: str = ""
    
    def add_exit(self, direction: str, target_x: int, target_y: int):
        """Add an exit to another room"""
        self.exits[direction] = (target_x, target_y)
    
    def get_available_exits(self) -> List[str]:
        """Get list of available exit directions"""
        return list(self.exits.keys())
    
    def describe_room(self) -> str:
        """Generate a description of the room"""
        if not self.visited:
            self.visited = True
            return f"You enter {self.name.lower()}. {self.description}"
        else:
            return f"You are in {self.name.lower()}. {self.description}" 