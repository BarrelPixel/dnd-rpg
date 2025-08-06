"""
Command handler for D&D 3.5e RPG
"""
from typing import Dict, Any, Callable, Optional, List
from utils import console, print_error, print_character_sheet, print_inventory
from models import Character
from spells import display_spell_list

class CommandHandler:
    """Handles player commands using the command pattern"""
    
    def __init__(self, game_state, dungeon_master):
        self.game_state = game_state
        self.dm = dungeon_master
        self.commands = self._register_commands()
    
    def _register_commands(self) -> Dict[str, Callable]:
        """Register all available commands"""
        return {
            'look': self._handle_look,
            'move': self._handle_move,
            'character': self._handle_character,
            'spells': self._handle_spells,
            'inventory': self._handle_inventory,
            'map': self._handle_map,
            'save': self._handle_save,
            'stats': self._handle_stats,
            'help': self._handle_help,
            'quit': self._handle_quit,
            'exit': self._handle_quit
        }
    
    def execute(self, command: str, character: Character, dungeon) -> bool:
        """
        Execute a command
        
        Args:
            command: The command to execute
            character: The player character
            dungeon: The current dungeon
            
        Returns:
            bool: True if the game should continue, False if it should quit
        """
        # Parse command and arguments
        parts = command.lower().strip().split()
        if not parts:
            return True
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Check if command exists
        if cmd in self.commands:
            try:
                return self.commands[cmd](character, dungeon, args)
            except Exception as e:
                print_error(f"Error executing command '{cmd}': {e}")
                return True
        else:
            print_error(f"Unknown command: {cmd}")
            console.print("Type 'help' for available commands.")
            return True
    
    def _handle_look(self, character: Character, dungeon, args) -> bool:
        """Handle 'look' command"""
        current_room = dungeon.get_current_room()
        console.print(f"\n[cyan]{current_room.description}[/cyan]")
        
        # Explore room for encounters/treasure
        from dungeon import explore_room
        enemies = explore_room(current_room, character.to_dict())
        if enemies:
            # Convert enemies back to Monster objects for combat
            from combat import start_combat
            updated_character = start_combat(character.to_dict(), enemies)
            character = Character.from_dict(updated_character)
            self.game_state.update_character(character.to_dict())
            
            # Check if character survived
            if not character.is_alive():
                return False  # Game over
        
        return True
    
    def _handle_move(self, character: Character, dungeon, args) -> bool:
        """Handle 'move [direction]' command"""
        if not args:
            print_error("Move where? Use: move north, move south, move east, move west")
            return True
        
        direction = args[0]
        if direction not in ['north', 'south', 'east', 'west']:
            print_error("Invalid direction. Use: north, south, east, west")
            return True
        
        if dungeon.move(direction):
            # Explore new room
            current_room = dungeon.get_current_room()
            from dungeon import explore_room
            enemies = explore_room(current_room, character.to_dict())
            if enemies:
                # Convert enemies back to Monster objects for combat
                from combat import start_combat
                updated_character = start_combat(character.to_dict(), enemies)
                character = Character.from_dict(updated_character)
                self.game_state.update_character(character.to_dict())
                
                # Check if character survived
                if not character.is_alive():
                    return False  # Game over
        
        return True
    
    def _handle_character(self, character: Character, dungeon, args) -> bool:
        """Handle 'character' command"""
        print_character_sheet(character.to_dict())
        return True
    
    def _handle_spells(self, character: Character, dungeon, args) -> bool:
        """Handle 'spells' command"""
        if character.character_class.value in ['Cleric', 'Wizard']:
            display_spell_list(character.to_dict())
        else:
            console.print("[yellow]You are not a spellcaster.[/yellow]")
        return True
    
    def _handle_inventory(self, character: Character, dungeon, args) -> bool:
        """Handle 'inventory' command"""
        print_inventory(character.inventory)
        return True
    
    def _handle_map(self, character: Character, dungeon, args) -> bool:
        """Handle 'map' command"""
        console.print(dungeon.get_dungeon_map())
        return True
    
    def _handle_save(self, character: Character, dungeon, args) -> bool:
        """Handle 'save' command"""
        self.game_state.save_game()
        return True
    
    def _handle_stats(self, character: Character, dungeon, args) -> bool:
        """Handle 'stats' command"""
        self.game_state.display_game_stats()
        return True
    
    def _handle_help(self, character: Character, dungeon, args) -> bool:
        """Handle 'help' command"""
        self._show_help()
        return True
    
    def _handle_quit(self, character: Character, dungeon, args) -> bool:
        """Handle 'quit' or 'exit' command"""
        console.print("\n[bold cyan]Thanks for playing D&D 3.5e Text-Based RPG![/bold cyan]")
        console.print("[italic]May your dice roll true![/italic]")
        return False  # Signal to quit
    
    def _show_help(self):
        """Show help information"""
        from utils import print_section_header, Prompt
        
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
    
    def get_available_commands(self) -> List[str]:
        """Get list of available commands for help"""
        return list(self.commands.keys()) 