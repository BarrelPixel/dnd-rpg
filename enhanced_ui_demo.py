"""
Enhanced UI Demo - Showcasing the new interface improvements
"""
from enhanced_ui import enhanced_ui
from utils import console, Prompt
import time

def demo_character_sheet():
    """Demo enhanced character sheet"""
    console.print("\n[bold cyan]=== Enhanced Character Sheet ===[/bold cyan]")
    
    # Create a sample character
    character = {
        'name': 'Erik the Cleric',
        'race': 'Human',
        'class': 'Cleric',
        'level': 3,
        'abilities': {
            'strength': 16,
            'dexterity': 12,
            'constitution': 14,
            'intelligence': 10,
            'wisdom': 18,
            'charisma': 8
        },
        'current_hp': 24,
        'max_hp': 24,
        'armor_class': 16,
        'initiative_bonus': 1,
        'experience': 3500,
        'inventory': {
            'Longsword': 1,
            'Chain Shirt': 1,
            'Potion of Healing': 3,
            'Holy Symbol': 1
        }
    }
    
    enhanced_ui.display_enhanced_character_sheet(character)
    Prompt.ask("\nPress Enter to continue")

def demo_combat_interface():
    """Demo enhanced combat interface"""
    console.print("\n[bold cyan]=== Enhanced Combat Interface ===[/bold cyan]")
    
    character = {
        'name': 'Erik',
        'class': 'Cleric',
        'level': 3,
        'race': 'Human',
        'current_hp': 18,
        'max_hp': 24,
        'armor_class': 16,
        'abilities': {'wisdom': 18}
    }
    
    enemies = [
        {'name': 'Goblin', 'current_hp': 3, 'max_hp': 6, 'armor_class': 15},
        {'name': 'Zombie', 'current_hp': 8, 'max_hp': 16, 'armor_class': 11}
    ]
    
    enhanced_ui.display_enhanced_combat(character, enemies, 3)
    Prompt.ask("\nPress Enter to continue")

def demo_progress_bars():
    """Demo progress bars"""
    console.print("\n[bold cyan]=== Progress Bars ===[/bold cyan]")
    
    character = {
        'current_hp': 18,
        'max_hp': 24,
        'experience': 3500
    }
    
    enhanced_ui.display_progress_bars(character)
    Prompt.ask("\nPress Enter to continue")

def demo_themes():
    """Demo different themes"""
    console.print("\n[bold cyan]=== Theme System ===[/bold cyan]")
    
    themes = ['classic', 'dark', 'fantasy', 'combat']
    
    for theme in themes:
        console.print(f"\n[bold]Theme: {theme.upper()}[/bold]")
        enhanced_ui.set_theme(theme)
        
        # Show a sample panel
        from rich.panel import Panel
        sample_panel = Panel(
            f"This is the {theme} theme!\n"
            f"Primary: {enhanced_ui.get_color('primary')}\n"
            f"Secondary: {enhanced_ui.get_color('secondary')}\n"
            f"Accent: {enhanced_ui.get_color('accent')}",
            title=f"{theme.title()} Theme",
            border_style=enhanced_ui.get_color('primary')
        )
        console.print(sample_panel)
        
        time.sleep(1)
    
    Prompt.ask("\nPress Enter to continue")

def demo_dungeon_map():
    """Demo dungeon map"""
    console.print("\n[bold cyan]=== Dungeon Map ===[/bold cyan]")
    
    current_room = {'x': 1, 'y': 1}
    visited_rooms = [(0, 0), (1, 0), (1, 1), (2, 1)]
    
    enhanced_ui.display_dungeon_map(current_room, visited_rooms)
    Prompt.ask("\nPress Enter to continue")

def demo_health_bars():
    """Demo health bars"""
    console.print("\n[bold cyan]=== Health Bars ===[/bold cyan]")
    
    health_levels = [
        (24, 24, "Full Health"),
        (18, 24, "Good Health"),
        (12, 24, "Moderate Health"),
        (6, 24, "Low Health"),
        (2, 24, "Critical Health")
    ]
    
    for current, maximum, description in health_levels:
        health_bar = enhanced_ui.create_health_bar(current, maximum, description)
        console.print(health_bar)
        time.sleep(0.5)
    
    Prompt.ask("\nPress Enter to continue")

def main():
    """Run all enhanced UI demos"""
    console.print("[bold blue]D&D 3.5e RPG - Enhanced UI Demo[/bold blue]")
    console.print("[dim]Showcasing the new interface improvements[/dim]\n")
    
    # Reset to classic theme
    enhanced_ui.set_theme("classic")
    
    demo_character_sheet()
    demo_combat_interface()
    demo_progress_bars()
    demo_themes()
    demo_dungeon_map()
    demo_health_bars()
    
    console.print("\n[bold green]Enhanced UI Demo Complete![/bold green]")
    console.print("[cyan]Try running the game and use the 'theme' command to change themes![/cyan]")

if __name__ == "__main__":
    main() 