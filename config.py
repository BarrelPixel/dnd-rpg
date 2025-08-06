"""
Configuration management for D&D 3.5e RPG
"""
import json
import os
from typing import Dict, Any
from pathlib import Path

class GameConfig:
    """Centralized game configuration management"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configurations
        self._default_config = {
            "game": {
                "name": "D&D 3.5e Text-Based RPG",
                "version": "1.0.0",
                "save_file": "save_game.json",
                "auto_save": True,
                "debug_mode": False
            },
            "character": {
                "starting_gold": 100,
                "max_level": 20,
                "xp_table": [0, 1000, 3000, 6000, 10000, 15000, 21000, 28000, 36000, 45000],
                "ability_score_method": "4d6_drop_lowest",
                "starting_hp_method": "max_first_level"
            },
            "combat": {
                "initiative_modifier": "dexterity",
                "critical_hit_threshold": 20,
                "critical_hit_multiplier": 2,
                "death_threshold": -10,
                "stabilization_check": "constitution"
            },
            "dungeon": {
                "min_rooms": 5,
                "max_rooms": 15,
                "boss_room_level": 3,
                "treasure_chance": 0.3,
                "encounter_chance": 0.4
            },
            "ai": {
                "enabled": True,
                "model": "gpt-3.5-turbo",
                "max_tokens": 150,
                "temperature": 0.7,
                "fallback_narration": True
            },
            "ui": {
                "colors_enabled": True,
                "show_dice_rolls": True,
                "show_combat_details": True,
                "pause_between_actions": True,
                "pause_duration": 1.0
            }
        }
        
        # Load configurations
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON files"""
        config = self._default_config.copy()
        
        # Load each configuration section
        for section in config.keys():
            config_file = self.config_dir / f"{section}.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        section_config = json.load(f)
                        config[section].update(section_config)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load {config_file}: {e}")
        
        return config
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """Set a configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def save_section(self, section: str):
        """Save a configuration section to JSON file"""
        config_file = self.config_dir / f"{section}.json"
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config[section], f, indent=2)
        except IOError as e:
            print(f"Error saving {config_file}: {e}")
    
    def reload(self):
        """Reload configuration from files"""
        self.config = self._load_config()
    


# Global configuration instance
config = GameConfig() 