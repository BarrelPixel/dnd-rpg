"""
Main game file for D&D RPG
"""
from typing import Dict, Optional
from models import Character, Abilities
from game_state import GameStateManager
from utils import roll_ability_score

class DnDRPG:
    """Main game class"""
    def __init__(self):
        self.game_state = GameStateManager()
        self.running = True
    
    def create_character(self) -> Character:
        """Create a new character"""
        print("\n=== Character Creation ===")
        name = input("Enter character name: ")
        
        # Simple race/class selection for now
        races = ["Human", "Elf", "Dwarf"]
        classes = ["Fighter", "Wizard", "Cleric"]
        
        print("\nAvailable races:")
        for i, race in enumerate(races, 1):
            print(f"{i}. {race}")
        race = races[int(input("Choose race (number): ")) - 1]
        
        print("\nAvailable classes:")
        for i, cls in enumerate(classes, 1):
            print(f"{i}. {cls}")
        char_class = classes[int(input("Choose class (number): ")) - 1]
        
        # Roll abilities
        print("\nRolling abilities...")
        abilities = Abilities(
            strength=roll_ability_score(),
            dexterity=roll_ability_score(),
            constitution=roll_ability_score(),
            intelligence=roll_ability_score(),
            wisdom=roll_ability_score(),
            charisma=roll_ability_score()
        )
        
        return Character(name=name, race=race, character_class=char_class, abilities=abilities)

    def main_menu(self) -> None:
        """Display main menu"""
        print("\n=== D&D RPG ===")
        print("1. New Game")
        print("2. Quit")
        
        choice = input("Choose an option: ")
        if choice == "1":
            character = self.create_character()
            self.game_state.new_game(character)
        elif choice == "2":
            self.running = False

    def game_loop(self) -> None:
        """Main game loop"""
        character = self.game_state.get_character()
        print(f"\nPlaying as {character.name} the {character.race} {character.character_class}")
        print(f"HP: {character.current_hp}/{character.max_hp}")
        
        # Simple command loop
        while self.running and character.is_alive():
            command = input("\nWhat would you like to do? (quit to exit): ")
            if command.lower() == "quit":
                self.running = False

    def run(self) -> None:
        """Run the game"""
        while self.running:
            if not self.game_state.is_game_active():
                self.main_menu()
        else:
                self.game_loop()

def main():
        game = DnDRPG()
        game.run()

if __name__ == "__main__":
    main() 