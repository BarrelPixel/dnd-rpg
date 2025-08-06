"""
Main game file for D&D 3.5e Text-Based RPG
"""
import os
import sys
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Import game modules
from utils import (
    print_title, print_section_header, print_choice_menu, 
    console, Prompt, print_narrative, dramatic_pause,
    print_success, print_error, print_info, print_warning
)
from character import create_character, print_character_sheet, is_character_alive
from combat import start_combat, create_monster
from dungeon import create_dungeon, explore_room
from dungeon_master import DungeonMaster
from game_state import GameState
from models import Character
from command_handler import CommandHandler

class DnDRPG:
    """Main game class that orchestrates all components"""
    
    def __init__(self):
        self.game_state = GameState()
        self.dm = DungeonMaster()
        self.command_handler = CommandHandler(self.game_state, self.dm)
        self.running = True
    
    def run(self):
        """Main game loop"""
        print_title()
        
        while self.running:
            if not self.game_state.is_game_started():
                self.show_main_menu()
            else:
                self.play_game()
    
    def show_main_menu(self):
        """Display the main menu"""
        print_section_header("Main Menu")
        
        options = ["Start New Game", "Load Game", "Help", "Quit"]
        
        if self.game_state.has_save_file():
            choice = print_choice_menu(options, "What would you like to do?")
        else:
            # Remove "Load Game" option if no save file exists
            options = ["Start New Game", "Help", "Quit"]
            choice = print_choice_menu(options, "What would you like to do?")
            if choice >= 1:  # Adjust choice index since we removed "Load Game"
                choice += 1
        
        if choice == 0:  # Start New Game
            self.start_new_game()
        elif choice == 1:  # Load Game
            if self.game_state.has_save_file():
                self.load_game()
            else:
                self.show_help()
        elif choice == 2:  # Help
            self.show_help()
        elif choice == 3:  # Quit
            self.quit_game()
    
    def start_new_game(self):
        """Start a new game"""
        print_section_header("Character Creation")
        
        # Create character
        character = create_character()
        
        # Start new game
        if self.game_state.start_new_game(character):
            # Create dungeon
            dungeon = create_dungeon()
            self.game_state.set_dungeon(dungeon)
            
            # Introduce adventure
            self.dm.introduce_adventure(character)
            
            print_success("Your adventure begins!")
            dramatic_pause(1.0)
    
    def load_game(self):
        """Load an existing game"""
        if self.game_state.load_game():
            character = self.game_state.get_character()
            dungeon = self.game_state.get_dungeon()
            
            if character and dungeon:
                print_success(f"Welcome back, {character['name']}!")
                console.print(f"You are in the dungeon at position {dungeon.current_position}")
            else:
                print_error("Save file is corrupted. Starting new game...")
                self.start_new_game()
        else:
            print_error("Failed to load game. Starting new game...")
            self.start_new_game()
    
    def show_help(self):
        """Show help information"""
        print_section_header("Help")
        
        console.print("[bold cyan]How to Play:[/bold cyan]")
        console.print("1. Create your character by choosing race and class")
        console.print("2. Roll ability scores (4d6, drop lowest)")
        console.print("3. Explore the dungeon using movement commands")
        console.print("4. Fight enemies in turn-based combat")
        console.print("5. Find treasure and gain experience")
        console.print("6. Reach the boss room to complete the adventure")
        
        console.print("\n[bold cyan]Game Commands:[/bold cyan]")
        console.print("- look: Examine your surroundings")
        console.print("- move [direction]: Move north, south, east, or west")
        console.print("- attack [target]: Attack an enemy")
        console.print("- cast [spell]: Cast a spell (if you're a spellcaster)")
        console.print("- spells: View your spell list (spellcasters only)")
        console.print("- inventory: Check your inventory")
        console.print("- character: View your character sheet")
        console.print("- map: Show dungeon map")
        console.print("- save: Save your game")
        console.print("- stats: Show game statistics")
        console.print("- help: Show this help")
        console.print("- quit: Exit the game")
        
        console.print("\n[bold cyan]D&D 3.5e Rules:[/bold cyan]")
        console.print("- Roll 1d20 + modifiers to hit enemies")
        console.print("- Roll damage dice when you hit")
        console.print("- Initiative determines turn order")
        console.print("- Armor Class (AC) determines how hard you are to hit")
        console.print("- Hit Points (HP) represent your health")
        
        Prompt.ask("\nPress Enter to continue")
    
    def play_game(self):
        """Main game play loop"""
        character_data = self.game_state.get_character()
        dungeon = self.game_state.get_dungeon()
        
        if not character_data or not dungeon:
            print_error("Game state error. Returning to main menu.")
            self.game_state.reset_game()
            return
        
        # Convert to Character object
        character = Character.from_dict(character_data)
        
        # Check if character is alive
        if not character.is_alive():
            print_error("Your character has been defeated!")
            self.handle_game_over(False)
            return
        
        # Check if at boss room
        if dungeon.is_at_boss_room():
            self.handle_boss_encounter(character, dungeon)
            return
        
        # Show current room
        current_room = dungeon.get_current_room()
        console.print(f"\n[bold cyan]Current Location: {current_room.name}[/bold cyan]")
        console.print(f"[cyan]{current_room.describe_room()}[/cyan]")
        
        # Show available exits
        exits = dungeon.get_available_moves()
        if exits:
            console.print(f"\n[green]Exits: {', '.join(exits)}[/green]")
        
        # Get player command
        command = Prompt.ask("\nWhat would you like to do?").strip()
        
        # Process command using command handler
        should_continue = self.command_handler.execute(command, character, dungeon)
        if not should_continue:
            self.quit_game()
    

    
    def handle_combat(self, character: Character, enemies: list):
        """Handle combat encounters"""
        self.game_state.increment_encounters()
        
        # DM describes combat start
        self.dm.describe_combat_start(enemies, character.to_dict())
        
        # Start combat
        updated_character = start_combat(character.to_dict(), enemies)
        
        # Update character in game state
        self.game_state.update_character(updated_character)
        
        # Check if character survived
        if not Character.from_dict(updated_character).is_alive():
            self.handle_game_over(False)
    
    def handle_boss_encounter(self, character: Character, dungeon):
        """Handle the final boss encounter"""
        console.print("\n[bold red]BOSS ENCOUNTER![/bold red]")
        
        # DM describes boss encounter
        self.dm.describe_boss_encounter(character.to_dict())
        
        # Create boss monster
        boss = create_monster("Orc")  # Use Orc as boss for now
        boss['name'] = "Dungeon Master"
        boss['max_hp'] = 20
        boss['current_hp'] = 20
        boss['armor_class'] = 16
        boss['attack_bonus'] = 5
        boss['damage'] = "1d10"
        boss['damage_bonus'] = 3
        boss['xp_value'] = 500
        
        # Start boss combat
        self.handle_combat(character, [boss])
        
        # Check if character defeated boss
        if character.is_alive():
            self.handle_game_over(True)
    
    def handle_game_over(self, victory: bool):
        """Handle game over"""
        character = self.game_state.get_character()
        
        if victory:
            self.dm.describe_adventure_end(character, True)
            self.game_state.mark_adventure_completed()
            print_success("Congratulations! You have completed the dungeon!")
        else:
            self.dm.describe_adventure_end(character, False)
            print_error("Game Over! Your character has been defeated.")
        
        # Show final stats
        self.game_state.display_game_stats()
        
        # Ask if player wants to play again
        options = ["Play Again", "Return to Main Menu", "Quit"]
        choice = print_choice_menu(options, "What would you like to do?")
        
        if choice == 0:  # Play Again
            self.game_state.reset_game()
            self.start_new_game()
        elif choice == 1:  # Return to Main Menu
            self.game_state.reset_game()
        else:  # Quit
            self.quit_game()
    
    def quit_game(self):
        """Quit the game"""
        console.print("\n[bold cyan]Thanks for playing D&D 3.5e Text-Based RPG![/bold cyan]")
        console.print("[italic]May your dice roll true![/italic]")
        self.running = False
        sys.exit(0)

def main():
    """Main entry point"""
    try:
        # Check if OpenAI API key is set
        if not os.getenv('OPENAI_API_KEY'):
            console.print("[yellow]Warning: No OpenAI API key found in .env file.[/yellow]")
            console.print("[yellow]The AI Dungeon Master will use fallback narration.[/yellow]")
            console.print("[yellow]To enable AI narration, create a .env file with: OPENAI_API_KEY=your_key_here[/yellow]")
            dramatic_pause(2.0)
        
        # Start the game
        game = DnDRPG()
        game.run()
    
    except KeyboardInterrupt:
        console.print("\n\n[red]Game interrupted by user.[/red]")
        sys.exit(0)
    
    except Exception as e:
        console.print(f"\n[red]An error occurred: {e}[/red]")
        console.print("[red]Please report this issue.[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 