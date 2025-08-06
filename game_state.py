"""
Game state management for D&D 3.5e RPG
"""
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from utils import console, print_success, print_error, print_info

class GameState:
    """Manages the overall game state and persistence"""
    
    def __init__(self):
        self.save_file = "save_game.json"
        self.game_data = {
            "character": None,
            "dungeon": None,
            "current_room": None,
            "game_started": False,
            "adventure_completed": False,
            "total_encounters": 0,
            "total_xp_gained": 0,
            "treasure_found": 0,
            "start_time": None,
            "last_save": None
        }
    
    def start_new_game(self, character: Dict[str, Any]) -> bool:
        """Start a new game with the given character"""
        try:
            self.game_data = {
                "character": character,
                "dungeon": None,
                "current_room": None,
                "game_started": True,
                "adventure_completed": False,
                "total_encounters": 0,
                "total_xp_gained": 0,
                "treasure_found": 0,
                "start_time": datetime.now().isoformat(),
                "last_save": datetime.now().isoformat()
            }
            
            print_success("New game started!")
            return True
        
        except Exception as e:
            print_error(f"Failed to start new game: {e}")
            return False
    
    def save_game(self) -> bool:
        """Save the current game state to file"""
        try:
            # Update last save time
            self.game_data["last_save"] = datetime.now().isoformat()
            
            # Convert dungeon object to serializable format
            save_data = self._serialize_game_data()
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print_success("Game saved successfully!")
            return True
        
        except Exception as e:
            print_error(f"Failed to save game: {e}")
            return False
    
    def load_game(self) -> bool:
        """Load game state from file"""
        try:
            if not os.path.exists(self.save_file):
                print_error("No save file found.")
                return False
            
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            # Restore game data
            self.game_data = self._deserialize_game_data(save_data)
            
            print_success("Game loaded successfully!")
            return True
        
        except Exception as e:
            print_error(f"Failed to load game: {e}")
            return False
    
    def _serialize_game_data(self) -> Dict[str, Any]:
        """Convert game data to JSON-serializable format"""
        serialized = self.game_data.copy()
        
        # Convert dungeon object to dict if it exists
        if serialized["dungeon"]:
            serialized["dungeon"] = self._serialize_dungeon(serialized["dungeon"])
        
        return serialized
    
    def _deserialize_game_data(self, save_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert saved data back to game format"""
        deserialized = save_data.copy()
        
        # Convert dungeon dict back to object if it exists
        if deserialized["dungeon"]:
            from dungeon import Dungeon
            deserialized["dungeon"] = self._deserialize_dungeon(deserialized["dungeon"])
        
        return deserialized
    
    def _serialize_dungeon(self, dungeon) -> Dict[str, Any]:
        """Serialize dungeon object to dict"""
        return {
            "width": dungeon.width,
            "height": dungeon.height,
            "current_position": dungeon.current_position,
            "entrance": dungeon.entrance,
            "boss_room": dungeon.boss_room,
            "rooms": self._serialize_rooms(dungeon.rooms)
        }
    
    def _deserialize_dungeon(self, dungeon_data: Dict[str, Any]):
        """Deserialize dungeon dict back to object"""
        from dungeon import Dungeon, DungeonRoom
        
        dungeon = Dungeon(dungeon_data["width"], dungeon_data["height"])
        dungeon.current_position = dungeon_data["current_position"]
        dungeon.entrance = dungeon_data["entrance"]
        dungeon.boss_room = dungeon_data["boss_room"]
        dungeon.rooms = self._deserialize_rooms(dungeon_data["rooms"])
        
        return dungeon
    
    def _serialize_rooms(self, rooms: Dict) -> Dict[str, Any]:
        """Serialize room objects to dict"""
        serialized_rooms = {}
        for pos, room in rooms.items():
            serialized_rooms[str(pos)] = {
                "room_type": room.room_type,
                "x": room.x,
                "y": room.y,
                "visited": room.visited,
                "exits": room.exits,
                "encounter": room.encounter,
                "treasure": room.treasure,
                "description": room.description,
                "name": room.name
            }
        return serialized_rooms
    
    def _deserialize_rooms(self, rooms_data: Dict[str, Any]) -> Dict:
        """Deserialize room dicts back to objects"""
        from dungeon import DungeonRoom
        
        rooms = {}
        for pos_str, room_data in rooms_data.items():
            # Convert pos string back to tuple
            pos = eval(pos_str)  # Safe for tuple conversion
            
            room = DungeonRoom(room_data["room_type"], room_data["x"], room_data["y"])
            room.visited = room_data["visited"]
            room.exits = room_data["exits"]
            room.encounter = room_data["encounter"]
            room.treasure = room_data["treasure"]
            room.description = room_data["description"]
            room.name = room_data["name"]
            
            rooms[pos] = room
        
        return rooms
    
    def update_character(self, character: Dict[str, Any]):
        """Update the character in game state"""
        self.game_data["character"] = character
    
    def set_dungeon(self, dungeon):
        """Set the current dungeon"""
        self.game_data["dungeon"] = dungeon
    
    def get_character(self) -> Optional[Dict[str, Any]]:
        """Get the current character"""
        return self.game_data["character"]
    
    def get_dungeon(self):
        """Get the current dungeon"""
        return self.game_data["dungeon"]
    
    def is_game_started(self) -> bool:
        """Check if a game is currently in progress"""
        return self.game_data["game_started"]
    
    def is_adventure_completed(self) -> bool:
        """Check if the adventure is completed"""
        return self.game_data["adventure_completed"]
    
    def mark_adventure_completed(self):
        """Mark the adventure as completed"""
        self.game_data["adventure_completed"] = True
        print_success("Adventure completed!")
    
    def increment_encounters(self):
        """Increment the encounter counter"""
        self.game_data["total_encounters"] += 1
    
    def add_xp(self, xp: int):
        """Add XP to the total gained"""
        self.game_data["total_xp_gained"] += xp
    
    def add_treasure(self, amount: int = 1):
        """Add to treasure found counter"""
        self.game_data["treasure_found"] += amount
    
    def get_game_stats(self) -> Dict[str, Any]:
        """Get current game statistics"""
        character = self.get_character()
        if not character:
            return {}
        
        return {
            "character_name": character["name"],
            "character_level": character["level"],
            "character_class": character["class"],
            "current_hp": character["current_hp"],
            "max_hp": character["max_hp"],
            "experience": character["experience"],
            "total_encounters": self.game_data["total_encounters"],
            "total_xp_gained": self.game_data["total_xp_gained"],
            "treasure_found": self.game_data["treasure_found"],
            "game_started": self.game_data["start_time"],
            "last_save": self.game_data["last_save"]
        }
    
    def display_game_stats(self):
        """Display current game statistics"""
        stats = self.get_game_stats()
        if not stats:
            print_info("No game in progress.")
            return
        
        console.print("\n[bold cyan]Game Statistics[/bold cyan]")
        console.print(f"Character: {stats['character_name']} (Level {stats['character_level']} {stats['character_class']})")
        console.print(f"Health: {stats['current_hp']}/{stats['max_hp']}")
        console.print(f"Experience: {stats['experience']}")
        console.print(f"Total Encounters: {stats['total_encounters']}")
        console.print(f"Total XP Gained: {stats['total_xp_gained']}")
        console.print(f"Treasure Found: {stats['treasure_found']}")
        
        if stats['game_started']:
            start_time = datetime.fromisoformat(stats['game_started'])
            console.print(f"Game Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if stats['last_save']:
            last_save = datetime.fromisoformat(stats['last_save'])
            console.print(f"Last Save: {last_save.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def reset_game(self):
        """Reset the game state"""
        self.game_data = {
            "character": None,
            "dungeon": None,
            "current_room": None,
            "game_started": False,
            "adventure_completed": False,
            "total_encounters": 0,
            "total_xp_gained": 0,
            "treasure_found": 0,
            "start_time": None,
            "last_save": None
        }
        
        # Remove save file if it exists
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        
        print_success("Game reset successfully!")
    
    def has_save_file(self) -> bool:
        """Check if a save file exists"""
        return os.path.exists(self.save_file) 