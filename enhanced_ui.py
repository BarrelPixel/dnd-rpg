"""
Enhanced UI components for D&D 3.5e RPG
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.box import ROUNDED, DOUBLE, HEAVY
from typing import Dict, Any, List
from utils import console

class EnhancedUI:
    """Enhanced UI components for better game presentation"""
    
    def __init__(self):
        self.console = console
        self.theme = "classic"  # classic, dark, fantasy, combat
        self.themes = {
            "classic": {
                "primary": "blue",
                "secondary": "green", 
                "accent": "yellow",
                "success": "green",
                "error": "red",
                "warning": "yellow",
                "info": "cyan"
            },
            "dark": {
                "primary": "white",
                "secondary": "dim white",
                "accent": "red",
                "success": "bright_green",
                "error": "bright_red",
                "warning": "bright_yellow",
                "info": "bright_cyan"
            },
            "fantasy": {
                "primary": "magenta",
                "secondary": "cyan",
                "accent": "bright_green",
                "success": "bright_green",
                "error": "bright_red",
                "warning": "bright_yellow",
                "info": "bright_cyan"
            },
            "combat": {
                "primary": "red",
                "secondary": "yellow",
                "accent": "white",
                "success": "bright_green",
                "error": "bright_red",
                "warning": "bright_yellow",
                "info": "bright_cyan"
            }
        }
    
    def get_color(self, color_type: str) -> str:
        """Get color from current theme"""
        return self.themes[self.theme].get(color_type, "white")
    
    def set_theme(self, theme: str):
        """Set the UI theme"""
        if theme in self.themes:
            self.theme = theme
    
    def create_character_panel(self, character: Dict[str, Any]) -> Panel:
        """Create an enhanced character status panel"""
        colors = self.themes[self.theme]
        
        # Character info
        char_info = f"[bold {colors['primary']}]{character['name']}[/bold {colors['primary']}]\n"
        char_info += f"Level {character['level']} {character['race']} {character['class']}\n"
        
        # Health bar
        hp_percent = (character['current_hp'] / character['max_hp']) * 100
        hp_color = "green" if hp_percent > 50 else "yellow" if hp_percent > 25 else "red"
        char_info += f"HP: [{hp_color}]{character['current_hp']}/{character['max_hp']}[/{hp_color}] "
        
        # Armor class
        char_info += f"AC: [{colors['secondary']}]{character['armor_class']}[/{colors['secondary']}]\n"
        
        # Spell slots for casters
        if character['class'] in ['Cleric', 'Wizard']:
            from spells import calculate_spell_slots
            spell_slots = calculate_spell_slots(character)
            slots_info = []
            for level, slots in spell_slots.items():
                if slots > 0:
                    slots_info.append(f"L{level}: {slots}")
            if slots_info:
                char_info += f"Spells: [{colors['accent']}]{', '.join(slots_info)}[/{colors['accent']}]"
        
        return Panel(
            char_info,
            title="Character Status",
            border_style=colors['primary'],
            box=ROUNDED
        )
    
    def create_combat_panel(self, enemies: List[Dict[str, Any]]) -> Panel:
        """Create an enhanced combat status panel"""
        colors = self.themes[self.theme]
        
        combat_info = ""
        for enemy in enemies:
            if enemy.get('current_hp', 0) > 0:
                hp_percent = (enemy['current_hp'] / enemy['max_hp']) * 100
                hp_color = "green" if hp_percent > 50 else "yellow" if hp_percent > 25 else "red"
                combat_info += f"[{colors['error']}]⚔️ {enemy['name']}[/{colors['error']}] "
                combat_info += f"[{hp_color}]{enemy['current_hp']}/{enemy['max_hp']}[/{hp_color}]\n"
        
        if not combat_info:
            combat_info = "[green]All enemies defeated![/green]"
        
        return Panel(
            combat_info,
            title="Combat Status",
            border_style=colors['error'],
            box=DOUBLE
        )
    
    def create_action_panel(self, actions: List[str]) -> Panel:
        """Create an action selection panel"""
        colors = self.themes[self.theme]
        
        action_text = ""
        for i, action in enumerate(actions, 1):
            action_text += f"[{colors['accent']}]{i}.[/{colors['accent']}] {action}\n"
        
        return Panel(
            action_text,
            title="Actions",
            border_style=colors['accent'],
            box=HEAVY
        )
    
    def create_health_bar(self, current: int, maximum: int, label: str = "Health") -> str:
        """Create a visual health bar"""
        if maximum <= 0:
            return f"{label}: 0/0"
        
        percentage = (current / maximum) * 100
        bar_length = 20
        filled_length = int((percentage / 100) * bar_length)
        
        # Choose color based on health percentage
        if percentage > 75:
            color = "green"
        elif percentage > 50:
            color = "yellow"
        elif percentage > 25:
            color = "orange"
        else:
            color = "red"
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"{label}: [{color}]{bar}[/{color}] {current}/{maximum} ({percentage:.0f}%)"
    
    def create_enhanced_combat_layout(self, character: Dict[str, Any], enemies: List[Dict[str, Any]], round_num: int) -> Layout:
        """Create an enhanced combat layout"""
        layout = Layout()
        
        # Split into header, main, and footer
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Split main into left and right
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # Split left into character and combat
        layout["left"].split_column(
            Layout(name="character"),
            Layout(name="combat")
        )
        
        # Split right into actions and log
        layout["right"].split_column(
            Layout(name="actions"),
            Layout(name="log")
        )
        
        # Add content
        colors = self.themes[self.theme]
        
        # Header
        header_text = f"[bold {colors['primary']}]COMBAT ROUND {round_num}[/bold {colors['primary']}]"
        layout["header"].update(Panel(header_text, border_style=colors['primary']))
        
        # Character panel
        layout["character"].update(self.create_character_panel(character))
        
        # Combat panel
        layout["combat"].update(self.create_combat_panel(enemies))
        
        # Actions panel
        actions = ["⚔️ Attack", "✨ Cast Spell", "📦 Use Item", "🏃 Flee"]
        layout["actions"].update(self.create_action_panel(actions))
        
        # Combat log
        log_text = "[dim]Combat log will appear here...[/dim]"
        layout["log"].update(Panel(log_text, title="Combat Log", border_style=colors['secondary']))
        
        # Footer
        footer_text = f"Commands: [1-4] Select action, [q] Quit"
        layout["footer"].update(Panel(footer_text, border_style=colors['secondary']))
        
        return layout
    
    def display_enhanced_combat(self, character: Dict[str, Any], enemies: List[Dict[str, Any]], round_num: int):
        """Display enhanced combat interface"""
        layout = self.create_enhanced_combat_layout(character, enemies, round_num)
        self.console.print(layout)
    
    def create_dungeon_map(self, current_room: Dict[str, Any], visited_rooms: List[tuple]) -> str:
        """Create an ASCII art dungeon map"""
        # Simple 3x3 grid representation
        map_grid = [
            ["   ", "   ", "   "],
            ["   ", "   ", "   "],
            ["   ", "   ", "   "]
        ]
        
        # Mark visited rooms
        for x, y in visited_rooms:
            if 0 <= x < 3 and 0 <= y < 3:
                map_grid[y][x] = " 🗺️ "
        
        # Mark current room
        current_x, current_y = current_room.get('x', 1), current_room.get('y', 1)
        if 0 <= current_x < 3 and 0 <= current_y < 3:
            map_grid[current_y][current_x] = " 👤 "
        
        # Create the map string
        map_str = "┌─────────┬─────────┬─────────┐\n"
        for i, row in enumerate(map_grid):
            map_str += "│" + "│".join(row) + "│\n"
            if i < 2:
                map_str += "├─────────┼─────────┼─────────┤\n"
        map_str += "└─────────┴─────────┴─────────┘\n"
        map_str += "\nLegend: 👤=You, 🗺️=Visited"
        
        return map_str
    
    def display_dungeon_map(self, current_room: Dict[str, Any], visited_rooms: List[tuple]):
        """Display dungeon map"""
        map_str = self.create_dungeon_map(current_room, visited_rooms)
        colors = self.themes[self.theme]
        
        panel = Panel(
            map_str,
            title="Dungeon Map",
            border_style=colors['accent'],
            box=ROUNDED
        )
        self.console.print(panel)
    
    def create_progress_bar(self, current: int, maximum: int, label: str, description: str = "") -> str:
        """Create a progress bar with rich formatting"""
        if maximum <= 0:
            return f"{label}: 0/0"
        
        percentage = (current / maximum) * 100
        bar_length = 30
        filled_length = int((percentage / 100) * bar_length)
        
        # Choose color based on percentage
        if percentage > 75:
            color = "green"
        elif percentage > 50:
            color = "yellow"
        elif percentage > 25:
            color = "orange"
        else:
            color = "red"
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        result = f"{label}: [{color}]{bar}[/{color}] {current}/{maximum}"
        if description:
            result += f" - {description}"
        
        return result
    
    def display_progress_bars(self, character: Dict[str, Any]):
        """Display progress bars for character stats"""
        colors = self.themes[self.theme]
        
        # Health bar
        health_bar = self.create_progress_bar(
            character['current_hp'], 
            character['max_hp'], 
            "Health"
        )
        
        # Experience bar (if we have XP data)
        xp_bar = self.create_progress_bar(
            character.get('experience', 0),
            1000,  # Next level threshold
            "Experience"
        )
        
        progress_panel = Panel(
            f"{health_bar}\n{xp_bar}",
            title="Status",
            border_style=colors['primary'],
            box=ROUNDED
        )
        
        self.console.print(progress_panel)

# Global enhanced UI instance
enhanced_ui = EnhancedUI() 