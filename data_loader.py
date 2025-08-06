"""
Data loader for D&D 3.5e RPG
"""
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


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
    
    def get_class(self, class_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific character class definition"""
        return self.classes.get(class_name)
    

    
    def reload(self):
        """Reload all data from files"""
        self._races = None
        self._classes = None
        self._monsters = None
        self._spells = None

# Global data loader instance
data_loader = DataLoader() 