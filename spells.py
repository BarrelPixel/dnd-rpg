"""
Spellcasting system for D&D 3.5e RPG
"""
import random
from typing import Dict, Any, List, Optional, Tuple
from utils import roll_dice, console, print_choice_menu, Prompt
from data_loader import data_loader
from config import config

# Get spell data from data loader
SPELLS = data_loader.spells

# Spell slots by class and level
SPELL_SLOTS = {
    "Cleric": {
        1: {"0": 3, "1": 1 + 1},  # Base + bonus for high Wisdom
        2: {"0": 3, "1": 2 + 1},
        3: {"0": 4, "1": 2 + 1, "2": 1 + 1},
        4: {"0": 4, "1": 3 + 1, "2": 2 + 1},
        5: {"0": 4, "1": 3 + 1, "2": 2 + 1, "3": 1 + 1}
    },
    "Wizard": {
        1: {"0": 3, "1": 1 + 1},  # Base + bonus for high Intelligence
        2: {"0": 3, "1": 2 + 1},
        3: {"0": 4, "1": 2 + 1, "2": 1 + 1},
        4: {"0": 4, "1": 3 + 1, "2": 2 + 1},
        5: {"0": 4, "1": 3 + 1, "2": 2 + 1, "3": 1 + 1}
    }
}

def get_spells_for_class(character_class: str) -> List[str]:
    """Get all spells available for a character class"""
    return [spell_name for spell_name, spell_data in SPELLS.items() 
            if spell_data["class"] == character_class]

def get_spells_by_level(character_class: str, spell_level: int) -> List[str]:
    """Get spells of a specific level for a character class"""
    return [spell_name for spell_name, spell_data in SPELLS.items() 
            if spell_data["class"] == character_class and spell_data["level"] == spell_level]

def calculate_spell_slots(character: Dict[str, Any]) -> Dict[str, int]:
    """Calculate spell slots for a character based on level and ability scores"""
    character_class = character["class"]
    level = character["level"]
    
    if character_class not in SPELL_SLOTS or level not in SPELL_SLOTS[character_class]:
        return {"0": 0, "1": 0}
    
    base_slots = SPELL_SLOTS[character_class][level].copy()
    
    # Add bonus spells for high ability scores
    if character_class == "Cleric":
        wisdom_mod = (character["abilities"]["wisdom"] - 10) // 2
        if wisdom_mod > 0:
            for spell_level in range(1, min(level + 1, 10)):
                if str(spell_level) in base_slots:
                    base_slots[str(spell_level)] += wisdom_mod
    elif character_class == "Wizard":
        int_mod = (character["abilities"]["intelligence"] - 10) // 2
        if int_mod > 0:
            for spell_level in range(1, min(level + 1, 10)):
                if str(spell_level) in base_slots:
                    base_slots[str(spell_level)] += int_mod
    
    return base_slots

def get_available_spells(character: Dict[str, Any]) -> Dict[str, List[str]]:
    """Get all spells available to a character, organized by level"""
    character_class = character["class"]
    available_spells = {}
    
    # Get spell slots
    spell_slots = calculate_spell_slots(character)
    
    # For each spell level the character has slots for
    for spell_level in spell_slots.keys():
        if spell_level == "0":
            # Cantrips/orisons (level 0 spells)
            available_spells["0"] = get_spells_by_level(character_class, 0)
        else:
            # Higher level spells
            level_int = int(spell_level)
            available_spells[spell_level] = get_spells_by_level(character_class, level_int)
    
    return available_spells

def cast_spell(character: Dict[str, Any], spell_name: str, target: Optional[Dict[str, Any]] = None) -> Tuple[bool, str, Optional[int]]:
    """Cast a spell and return (success, message, effect_value)"""
    if spell_name not in SPELLS:
        return False, f"Unknown spell: {spell_name}", None
    
    spell = SPELLS[spell_name]
    spell_level = spell["level"]
    
    # Check if character has spell slots available
    spell_slots = calculate_spell_slots(character)
    if str(spell_level) not in spell_slots or spell_slots[str(spell_level)] <= 0:
        return False, f"No spell slots available for level {spell_level} spells", None
    
    # Cast the spell based on its effect
    if spell["effect"] == "heal":
        if target is None:
            target = character
        
        heal_amount = roll_dice(spell["heal_amount"])
        old_hp = target["current_hp"]
        target["current_hp"] = min(target["max_hp"], target["current_hp"] + heal_amount)
        actual_heal = target["current_hp"] - old_hp
        
        message = f"{character['name']} casts {spell_name} on {target['name']}, healing {actual_heal} hit points!"
        effect_value = actual_heal
        
    elif spell["effect"] == "damage":
        if target is None:
            return False, f"{spell_name} requires a target", None
        
        damage_amount = roll_dice(spell["damage_amount"])
        damage_type = spell.get("damage_type", "magical")
        
        old_hp = target["current_hp"]
        target["current_hp"] = max(0, target["current_hp"] - damage_amount)
        actual_damage = old_hp - target["current_hp"]
        
        message = f"{character['name']} casts {spell_name} on {target['name']}, dealing {actual_damage} {damage_type} damage!"
        effect_value = actual_damage
        
    elif spell["effect"] == "buff":
        if target is None:
            target = character
        
        buff_type = spell.get("buff_type", "general")
        bonus = spell.get("bonus", 1)
        
        message = f"{character['name']} casts {spell_name} on {target['name']}, granting a +{bonus} {buff_type} bonus!"
        effect_value = bonus
        
    elif spell["effect"] == "status":
        if target is None:
            return False, f"{spell_name} requires a target", None
        
        status_type = spell.get("status_type", "special")
        message = f"{character['name']} casts {spell_name} on {target['name']}, applying {status_type} effect!"
        effect_value = None
        
    else:  # utility
        message = f"{character['name']} casts {spell_name}!"
        effect_value = None
    
    # Consume spell slot
    spell_slots[str(spell_level)] -= 1
    return True, message, effect_value

def display_spell_list(character: Dict[str, Any]):
    """Display the character's available spells"""
    console.print(f"\n[bold cyan]Spell List for {character['name']}[/bold cyan]")
    
    available_spells = get_available_spells(character)
    spell_slots = calculate_spell_slots(character)
    
    for level, spells in available_spells.items():
        if spells:
            console.print(f"\n[bold yellow]Level {level} Spells:[/bold yellow]")
            slots_available = spell_slots.get(level, 0)
            console.print(f"Slots available: {slots_available}")
            
            for spell_name in spells:
                spell = SPELLS[spell_name]
                console.print(f"  - {spell_name} ({spell['school']})")
                console.print(f"    {spell['description']}")

def select_spell_to_cast(character: Dict[str, Any]) -> Optional[str]:
    """Let the player select a spell to cast"""
    available_spells = get_available_spells(character)
    spell_slots = calculate_spell_slots(character)
    
    # Flatten available spells into a list
    spell_choices = []
    for level, spells in available_spells.items():
        slots = spell_slots.get(level, 0)
        if slots > 0 and spells:
            for spell_name in spells:
                spell_choices.append(f"{spell_name} (Level {level})")
    
    if not spell_choices:
        console.print("[yellow]No spells available to cast.[/yellow]")
        return None
    
    spell_choices.append("Cancel")
    
    choice_index = print_choice_menu(spell_choices, "Select a spell to cast:")
    
    if choice_index == len(spell_choices) - 1:  # Cancel
        return None
    
    selected_spell = spell_choices[choice_index].split(" (Level")[0]
    return selected_spell

def get_spell_info(spell_name: str) -> str:
    """Get detailed information about a spell"""
    if spell_name not in SPELLS:
        return f"Unknown spell: {spell_name}"
    
    spell = SPELLS[spell_name]
    info = f"[bold]{spell_name}[/bold]\n"
    info += f"Level: {spell['level']}\n"
    info += f"School: {spell['school']}\n"
    info += f"Casting Time: {spell['casting_time']}\n"
    info += f"Range: {spell['range']}\n"
    info += f"Target: {spell['target']}\n"
    info += f"Duration: {spell['duration']}\n"
    info += f"Saving Throw: {spell['saving_throw']}\n"
    info += f"Spell Resistance: {spell['spell_resistance']}\n"
    info += f"Description: {spell['description']}"
    
    return info 