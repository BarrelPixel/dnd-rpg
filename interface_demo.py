"""
Interface Demo - Showcasing visual options for terminal-based D&D RPG
"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.columns import Columns
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.emoji import Emoji
import time
import random

console = Console()

def demo_basic_styling():
    """Demo basic text styling"""
    console.print("\n[bold cyan]=== Basic Text Styling ===[/bold cyan]")
    
    console.print("[bold red]Bold Red Text[/bold red]")
    console.print("[italic green]Italic Green Text[/italic green]")
    console.print("[underline blue]Underlined Blue Text[/underline blue]")
    console.print("[strike yellow]Strikethrough Yellow Text[/strike yellow]")
    console.print("[reverse magenta]Reversed Magenta Text[/reverse magenta]")
    console.print("[dim white]Dim White Text[/dim white]")

def demo_panels():
    """Demo panel layouts"""
    console.print("\n[bold cyan]=== Panels ===[/bold cyan]")
    
    # Character info panel
    character_panel = Panel(
        "[bold]Erik the Cleric[/bold]\n"
        "Level 3 Human Cleric\n"
        "HP: 24/24 | AC: 16\n"
        "Spells: 4/4 Level 1",
        title="Character Status",
        border_style="green",
        box=ROUNDED
    )
    
    # Combat panel
    combat_panel = Panel(
        "[red]⚔️ Goblin[/red] HP: 3/6\n"
        "[red]⚔️ Goblin[/red] HP: 6/6\n"
        "[green]✅ Erik[/green] HP: 24/24",
        title="Combat Status",
        border_style="red",
        box=DOUBLE
    )
    
    # Spell panel
    spell_panel = Panel(
        "[magenta]✨ Cure Light Wounds[/magenta]\n"
        "Level 1 • Healing\n"
        "Touch • 1d8+1 HP",
        title="Spell Info",
        border_style="magenta",
        box=HEAVY
    )
    
    # Display panels in columns
    columns = Columns([character_panel, combat_panel, spell_panel])
    console.print(columns)

def demo_tables():
    """Demo table layouts"""
    console.print("\n[bold cyan]=== Tables ===[/bold cyan]")
    
    # Character sheet table
    char_table = Table(title="Character Sheet", box=ROUNDED)
    char_table.add_column("Attribute", style="cyan", no_wrap=True)
    char_table.add_column("Value", style="green")
    char_table.add_column("Modifier", style="yellow")
    
    char_table.add_row("Strength", "16", "+3")
    char_table.add_row("Dexterity", "12", "+1")
    char_table.add_row("Constitution", "14", "+2")
    char_table.add_row("Intelligence", "10", "+0")
    char_table.add_row("Wisdom", "18", "+4")
    char_table.add_row("Charisma", "8", "-1")
    
    console.print(char_table)
    
    # Inventory table
    inv_table = Table(title="Inventory", box=DOUBLE)
    inv_table.add_column("Item", style="cyan")
    inv_table.add_column("Quantity", style="green")
    inv_table.add_column("Weight", style="yellow")
    inv_table.add_column("Value", style="magenta")
    
    inv_table.add_row("Longsword", "1", "4 lbs", "15 gp")
    inv_table.add_row("Chain Shirt", "1", "25 lbs", "100 gp")
    inv_table.add_row("Potion of Healing", "3", "0.5 lbs", "50 gp each")
    inv_table.add_row("Backpack", "1", "2 lbs", "2 gp")
    
    console.print(inv_table)

def demo_layouts():
    """Demo layout system"""
    console.print("\n[bold cyan]=== Layouts ===[/bold cyan]")
    
    # Create a layout
    layout = Layout()
    
    # Split into top and bottom
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    # Split main into left and right
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    # Split left into top and bottom
    layout["left"].split_column(
        Layout(name="character"),
        Layout(name="combat")
    )
    
    # Add content to each section
    layout["header"].update(Panel("D&D 3.5e Text-Based RPG", style="bold blue"))
    layout["character"].update(Panel("Character Info\nHP: 24/24\nAC: 16", title="Character"))
    layout["combat"].update(Panel("Combat\nEnemies: 2\nStatus: Fighting", title="Combat"))
    layout["right"].update(Panel("Map\nYou are in a dark dungeon...", title="Location"))
    layout["footer"].update(Panel("Commands: look, move, attack, cast, inventory", title="Help"))
    
    console.print(layout)

def demo_progress_bars():
    """Demo progress bars and spinners"""
    console.print("\n[bold cyan]=== Progress Bars ===[/bold cyan]")
    
    # Health bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        # Health bar
        health_task = progress.add_task("Health", total=24)
        progress.update(health_task, completed=18, description="Health: 18/24")
        
        # Experience bar
        xp_task = progress.add_task("Experience", total=6000)
        progress.update(xp_task, completed=3500, description="XP: 3500/6000")
        
        # Spell casting progress
        spell_task = progress.add_task("Casting Magic Missile", total=100)
        for i in range(0, 101, 10):
            progress.update(spell_task, completed=i)
            time.sleep(0.1)

def demo_animations():
    """Demo live updates and animations"""
    console.print("\n[bold cyan]=== Live Updates ===[/bold cyan]")
    
    # Combat animation
    with Live(Panel("Combat starting..."), refresh_per_second=4) as live:
        for i in range(5):
            live.update(Panel(f"Round {i+1}\nErik attacks Goblin..."))
            time.sleep(0.5)
            live.update(Panel(f"Round {i+1}\nGoblin takes 8 damage!"))
            time.sleep(0.5)

def demo_ascii_art():
    """Demo ASCII art and symbols"""
    console.print("\n[bold cyan]=== ASCII Art & Symbols ===[/bold cyan]")
    
    # Simple dungeon map
    dungeon_map = """
    ┌─────────┬─────────┬─────────┐
    │   ⚔️    │         │         │
    │  Goblin │    🗺️   │    💎   │
    │         │   Map   │ Treasure│
    ├─────────┼─────────┼─────────┤
    │         │    👤   │         │
    │    🚪   │   Erik  │    🚪   │
    │   Door  │         │   Door  │
    ├─────────┼─────────┼─────────┤
    │         │         │    ⚔️   │
    │    🗝️   │    🗺️   │  Orc   │
    │   Key   │   Map   │         │
    └─────────┴─────────┴─────────┘
    """
    
    console.print(Panel(dungeon_map, title="Dungeon Map", border_style="yellow"))

def demo_interactive_elements():
    """Demo interactive elements"""
    console.print("\n[bold cyan]=== Interactive Elements ===[/bold cyan]")
    
    # Choice menu with icons
    choices = [
        "⚔️ Attack the goblin",
        "🛡️ Defend yourself", 
        "✨ Cast a spell",
        "🏃 Run away",
        "💬 Talk to the goblin"
    ]
    
    console.print("[bold yellow]What would you like to do?[/bold yellow]")
    for i, choice in enumerate(choices, 1):
        console.print(f"[cyan]{i}.[/cyan] {choice}")
    
    # Simulate user choice
    console.print("\n[dim]User selects: 3[/dim]")
    console.print("[magenta]✨ You begin casting Magic Missile![/magenta]")

def demo_color_themes():
    """Demo different color themes"""
    console.print("\n[bold cyan]=== Color Themes ===[/bold cyan]")
    
    themes = {
        "Classic": {"primary": "blue", "secondary": "green", "accent": "yellow"},
        "Dark": {"primary": "white", "secondary": "dim white", "accent": "red"},
        "Fantasy": {"primary": "magenta", "secondary": "cyan", "accent": "bright_green"},
        "Combat": {"primary": "red", "secondary": "yellow", "accent": "white"}
    }
    
    for theme_name, colors in themes.items():
        console.print(f"\n[bold {colors['primary']}]{theme_name} Theme:[/bold {colors['primary']}]")
        console.print(f"[{colors['secondary']}]This is secondary text[/{colors['secondary']}]")
        console.print(f"[{colors['accent']}]This is accent text[/{colors['accent']}]")

def demo_advanced_features():
    """Demo advanced rich features"""
    console.print("\n[bold cyan]=== Advanced Features ===[/bold cyan]")
    
    # Syntax highlighting for spell descriptions
    spell_code = """
    Spell: Magic Missile
    Level: 1
    School: Evocation
    Range: Medium (100 ft. + 10 ft./level)
    Duration: Instantaneous
    """
    
    syntax = Syntax(spell_code, "yaml", theme="monokai")
    console.print(Panel(syntax, title="Spell Description"))
    
    # Markdown rendering
    markdown_text = """
    # D&D 3.5e RPG
    
    ## Welcome to the Adventure!
    
    You are **Erik the Cleric**, a brave adventurer exploring the depths of the dungeon.
    
    ### Your Mission
    1. Find the ancient artifact
    2. Defeat the dungeon boss
    3. Escape with your life
    
    > *"Adventure awaits those who dare to enter..."*
    """
    
    md = Markdown(markdown_text)
    console.print(Panel(md, title="Game Introduction"))

def main():
    """Run all interface demos"""
    console.print("[bold blue]D&D 3.5e RPG - Interface Demo[/bold blue]")
    console.print("[dim]Showing all available visual options[/dim]\n")
    
    demo_basic_styling()
    demo_panels()
    demo_tables()
    demo_layouts()
    demo_progress_bars()
    demo_animations()
    demo_ascii_art()
    demo_interactive_elements()
    demo_color_themes()
    demo_advanced_features()
    
    console.print("\n[bold green]Interface Demo Complete![/bold green]")

if __name__ == "__main__":
    main() 