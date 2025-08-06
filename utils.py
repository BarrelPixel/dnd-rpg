"""
Utility functions for the D&D 3.5e RPG
"""
import random
import time
from typing import List, Dict, Any
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def roll_dice(dice_string: str) -> int:
    """
    Roll dice in D&D format (e.g., "3d6", "1d20+5")
    """
    try:
        # Parse dice string like "3d6+5" or "1d20"
        if '+' in dice_string:
            dice_part, modifier = dice_string.split('+')
            modifier = int(modifier)
        elif '-' in dice_string:
            dice_part, modifier = dice_string.split('-')
            modifier = -int(modifier)
        else:
            dice_part = dice_string
            modifier = 0
        
        if 'd' in dice_part:
            num_dice, die_size = map(int, dice_part.split('d'))
            result = sum(random.randint(1, die_size) for _ in range(num_dice)) + modifier
        else:
            result = int(dice_part) + modifier
        
        return result
    except:
        console.print(f"[red]Invalid dice format: {dice_string}[/red]")
        return 0

def roll_ability_score() -> int:
    """Roll 4d6, drop lowest, for ability scores"""
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))
    return sum(rolls)

def calculate_modifier(score: int) -> int:
    """Calculate ability modifier from ability score"""
    return (score - 10) // 2

def print_title():
    """Display the game title"""
    title = Text("D&D 3.5e Text-Based RPG", style="bold blue")
    subtitle = Text("Adventure Awaits!", style="italic green")
    
    console.print(Panel(title, subtitle=subtitle, border_style="blue"))

def print_section_header(text: str):
    """Print a section header"""
    console.print(f"\n[bold cyan]{'='*50}[/bold cyan]")
    console.print(f"[bold cyan]{text}[/bold cyan]")
    console.print(f"[bold cyan]{'='*50}[/bold cyan]\n")

def print_choice_menu(options: List[str], title: str = "Choose an option:") -> int:
    """Display a numbered choice menu and return the selected index"""
    console.print(f"\n[bold yellow]{title}[/bold yellow]")
    
    for i, option in enumerate(options, 1):
        console.print(f"[cyan]{i}.[/cyan] {option}")
    
    while True:
        try:
            choice = int(Prompt.ask("\nEnter your choice", default="1"))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

def print_character_sheet(character: Dict[str, Any]):
    """Display a formatted character sheet using enhanced UI"""
    try:
        from enhanced_ui import enhanced_ui
        enhanced_ui.display_enhanced_character_sheet(character)
    except ImportError:
        # Fallback to simple table
        _print_simple_character_sheet(character)

def _print_simple_character_sheet(character: Dict[str, Any]):
    """Fallback simple character sheet display"""
    table = Table(title=f"Character Sheet - {character['name']}")
    
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")
    
    # Basic info
    table.add_row("Name", character['name'])
    table.add_row("Class", character['class'])
    table.add_row("Level", str(character['level']))
    table.add_row("Race", character['race'])
    
    # Ability scores
    for ability in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
        score = character['abilities'][ability.lower()]
        modifier = calculate_modifier(score)
        modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
        table.add_row(ability, f"{score} ({modifier_str})")
    
    # Combat stats
    table.add_row("Hit Points", f"{character['current_hp']}/{character['max_hp']}")
    table.add_row("Armor Class", str(character['armor_class']))
    table.add_row("Initiative", f"+{character['initiative_bonus']}")
    
    console.print(table)

def print_combat_status(combatants: List[Dict[str, Any]]):
    """Display current combat status using enhanced UI"""
    try:
        from enhanced_ui import enhanced_ui
        
        # Separate character and enemies
        character = None
        enemies = []
        
        for combatant in combatants:
            if 'class' in combatant:  # This is the player character
                character = combatant
            else:  # This is an enemy
                enemies.append(combatant)
        
        if character:
            # Use enhanced UI for better display
            enhanced_ui.display_enhanced_combat(character, enemies, 1)  # Round number will be updated by caller
        else:
            # Fallback to simple table
            _print_simple_combat_status(combatants)
    except ImportError:
        # Fallback if enhanced UI is not available
        _print_simple_combat_status(combatants)

def _print_simple_combat_status(combatants: List[Dict[str, Any]]):
    """Fallback simple combat status display"""
    table = Table(title="Combat Status")
    
    table.add_column("Name", style="cyan")
    table.add_column("HP", style="red")
    table.add_column("AC", style="yellow")
    table.add_column("Status", style="green")
    
    for combatant in combatants:
        status = "Alive" if combatant['current_hp'] > 0 else "Unconscious"
        table.add_row(
            combatant['name'],
            f"{combatant['current_hp']}/{combatant['max_hp']}",
            str(combatant['armor_class']),
            status
        )
    
    console.print(table)

def print_inventory(inventory: Dict[str, int]):
    """Display character inventory"""
    if not inventory:
        console.print("[yellow]Your inventory is empty.[/yellow]")
        return
    
    table = Table(title="Inventory")
    table.add_column("Item", style="cyan")
    table.add_column("Quantity", style="green")
    
    for item, quantity in inventory.items():
        table.add_row(item, str(quantity))
    
    console.print(table)



def dramatic_pause(seconds: float = 1.0):
    """Add a dramatic pause to the narrative"""
    time.sleep(seconds)

def print_narrative(text: str, color: str = "white"):
    """Print narrative text with optional color"""
    console.print(f"[{color}]{text}[/{color}]")

def print_success(text: str):
    """Print success message"""
    console.print(f"[green]✓ {text}[/green]")

def print_error(text: str):
    """Print error message"""
    console.print(f"[red]✗ {text}[/red]")

def print_warning(text: str):
    """Print warning message"""
    console.print(f"[yellow]⚠ {text}[/yellow]")

def print_info(text: str):
    """Print info message"""
    console.print(f"[blue]ℹ {text}[/blue]") 