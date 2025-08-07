"""
Game state management for D&D RPG
"""
import json
from typing import Dict, Optional
from models import Character, GameState

class GameStateManager:
    def __init__(self):
        self.state = GameState()
        self.data_path = "data/"

    def load_data(self, filename: str) -> Dict:
        """Load JSON data file"""
        with open(f"{self.data_path}{filename}") as f:
            return json.load(f)

    def new_game(self, character: Character) -> None:
        """Start a new game with given character"""
        self.state.character = character
        self.state.game_started = True
        self.state.current_room = None

    def get_character(self) -> Optional[Character]:
        """Get current character"""
        return self.state.character

    def is_game_active(self) -> bool:
        """Check if game is active"""
        return self.state.is_game_active()

    def update_character(self, character: Character) -> None:
        """Update character in game state"""
        self.state.character = character