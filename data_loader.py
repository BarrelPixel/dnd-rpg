"""
Data loader for D&D 3.5e RPG
"""
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from models import Race, CharacterClass, SpellSchool, SpellEffect, Spell

class DataLoader:
    """Loads game data from JSON files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._races = None
        self._classes = None
        self._monsters = None
        self._spells = None
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load a JSON file from the data directory"""
        file_path = self.data_dir / filename
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    @property
    def races(self) -> Dict[str, Any]:
        """Get race definitions"""
        if self._races is None:
            self._races = self._load_json_file("races.json")
        return self._races
    
    @property
    def classes(self) -> Dict[str, Any]:
        """Get character class definitions"""
        if self._classes is None:
            self._classes = self._load_json_file("classes.json")
        return self._classes
    
    @property
    def monsters(self) -> Dict[str, Any]:
        """Get monster definitions"""
        if self._monsters is None:
            self._monsters = self._load_json_file("monsters.json")
        return self._monsters
    
    @property
    def spells(self) -> Dict[str, Any]:
        """Get spell definitions"""
        if self._spells is None:
            self._spells = self._load_json_file("spells.json")
        return self._spells
    
    def get_race(self, race_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific race definition"""
        return self.races.get(race_name)
    
    def get_class(self, class_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific character class definition"""
        return self.classes.get(class_name)
    
    def get_monster(self, monster_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific monster definition"""
        return self.monsters.get(monster_name)
    
    def get_spell(self, spell_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific spell definition"""
        return self.spells.get(spell_name)
    
    def get_available_races(self) -> List[str]:
        """Get list of available races"""
        return list(self.races.keys())
    
    def get_available_classes(self) -> List[str]:
        """Get list of available character classes"""
        return list(self.classes.keys())
    
    def get_available_monsters(self) -> List[str]:
        """Get list of available monsters"""
        return list(self.monsters.keys())
    
    def get_available_spells(self) -> List[str]:
        """Get list of available spells"""
        return list(self.spells.keys())
    
    def get_spells_by_class(self, character_class: str) -> List[str]:
        """Get spells available to a specific character class"""
        return [
            spell_name for spell_name, spell_data in self.spells.items()
            if spell_data.get("class") == character_class
        ]
    
    def get_spells_by_level(self, character_class: str, level: int) -> List[str]:
        """Get spells of a specific level for a character class"""
        return [
            spell_name for spell_name, spell_data in self.spells.items()
            if spell_data.get("class") == character_class and spell_data.get("level") == level
        ]
    
    def get_monsters_by_level(self, level: int) -> List[str]:
        """Get monsters of a specific level"""
        return [
            monster_name for monster_name, monster_data in self.monsters.items()
            if monster_data.get("level") == level
        ]
    
    def create_spell_object(self, spell_name: str) -> Optional[Spell]:
        """Create a Spell object from spell data"""
        spell_data = self.get_spell(spell_name)
        if not spell_data:
            return None
        
        try:
            return Spell(
                name=spell_data["name"],
                level=spell_data["level"],
                school=SpellSchool(spell_data["school"]),
                subschool=spell_data["subschool"],
                casting_time=spell_data["casting_time"],
                range=spell_data["range"],
                target=spell_data["target"],
                duration=spell_data["duration"],
                saving_throw=spell_data["saving_throw"],
                spell_resistance=spell_data["spell_resistance"],
                description=spell_data["description"],
                effect=SpellEffect(spell_data["effect"]),
                character_class=CharacterClass(spell_data["class"]),
                heal_amount=spell_data.get("heal_amount"),
                damage_amount=spell_data.get("damage_amount"),
                damage_type=spell_data.get("damage_type"),
                buff_type=spell_data.get("buff_type"),
                bonus=spell_data.get("bonus"),
                status_type=spell_data.get("status_type"),
                area_effect=spell_data.get("area_effect", False)
            )
        except (KeyError, ValueError) as e:
            print(f"Error creating spell object for {spell_name}: {e}")
            return None
    
    def reload(self):
        """Reload all data from files"""
        self._races = None
        self._classes = None
        self._monsters = None
        self._spells = None

# Global data loader instance
data_loader = DataLoader() 