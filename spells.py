"""
Spellcasting system for D&D 3.5e RPG
"""
import random
from typing import Dict, Any, List, Optional, Tuple
from utils import roll_dice, console, print_choice_menu, Prompt

# D&D 3.5e Spells
SPELLS = {
    # Cleric Cantrips (Level 0)
    "Light": {
        "name": "Light",
        "level": 0,
        "school": "Evocation",
        "subschool": "",
        "casting_time": "Standard Action",
        "range": "Touch",
        "target": "Object touched",
        "duration": "10 min./level (D)",
        "saving_throw": "None",
        "spell_resistance": "No",
        "description": "This spell causes an object to glow like a torch, shedding bright light in a 20-foot radius.",
        "effect": "utility",
        "class": "Cleric"
    },
    "Resistance": {
        "name": "Resistance",
        "level": 0,
        "school": "Abjuration",
        "subschool": "",
        "casting_time": "Standard Action",
        "range": "Touch",
        "target": "Creature touched",
        "duration": "1 minute",
        "saving_throw": "Will negates (harmless)",
        "spell_resistance": "Yes (harmless)",
        "description": "You imbue the subject with magical energy that protects it from harm, granting it a +1 resistance bonus on saves.",
        "effect": "buff",
        "buff_type": "saves",
        "bonus": 1,
        "class": "Cleric"
    },
    
    # Wizard Cantrips (Level 0)
    "Acid Splash": {
        "name": "Acid Splash",
        "level": 0,
        "school": "Conjuration",
        "subschool": "Creation",
        "casting_time": "Standard Action",
        "range": "Close (25 ft. + 5 ft./2 levels)",
        "target": "One creature",
        "duration": "Instantaneous",
        "saving_throw": "None",
        "spell_resistance": "Yes",
        "description": "You fire a small orb of acid at the target. You must succeed on a ranged touch attack to hit your target.",
        "effect": "damage",
        "damage_amount": "1d3",
        "damage_type": "Acid",
        "class": "Wizard"
    },
    "Daze": {
        "name": "Daze",
        "level": 0,
        "school": "Enchantment",
        "subschool": "Compulsion",
        "casting_time": "Standard Action",
        "range": "Close (25 ft. + 5 ft./2 levels)",
        "target": "One humanoid creature of 4 HD or less",
        "duration": "1 round",
        "saving_throw": "Will negates",
        "spell_resistance": "Yes",
        "description": "This spell clouds the mind of a humanoid creature with 4 or fewer Hit Dice so that it takes no actions.",
        "effect": "status",
        "status_type": "daze",
        "duration": "1 round",
        "class": "Wizard"
    },
    
    # Cleric Spells
    "Cure Light Wounds": {
        "name": "Cure Light Wounds",
        "level": 1,
        "school": "Conjuration",
        "subschool": "Healing",
        "casting_time": "Standard Action",
        "range": "Touch",
        "target": "Creature touched",
        "duration": "Instantaneous",
        "saving_throw": "Will half (harmless)",
        "spell_resistance": "Yes (harmless)",
        "description": "When laying your hand upon a living creature, you channel positive energy that cures 1d8 points of damage +1 point per caster level (maximum +5).",
        "effect": "heal",
        "heal_amount": "1d8+1",
        "class": "Cleric"
    },
    "Inflict Light Wounds": {
        "name": "Inflict Light Wounds",
        "level": 1,
        "school": "Necromancy",
        "subschool": "",
        "casting_time": "Standard Action",
        "range": "Touch",
        "target": "Creature touched",
        "duration": "Instantaneous",
        "saving_throw": "Will half",
        "spell_resistance": "Yes",
        "description": "When laying your hand upon a creature, you channel negative energy that deals 1d8 points of damage +1 point per caster level (maximum +5).",
        "effect": "damage",
        "damage_amount": "1d8+1",
        "damage_type": "Negative Energy",
        "class": "Cleric"
    },
    "Bless": {
        "name": "Bless",
        "level": 1,
        "school": "Enchantment",
        "subschool": "Compulsion",
        "casting_time": "Standard Action",
        "range": "50 ft.",
        "target": "Allies within 50 ft.",
        "duration": "1 min./level",
        "saving_throw": "None",
        "spell_resistance": "Yes (harmless)",
        "description": "Bless fills your allies with courage. Each affected creature gains a +1 morale bonus on attack rolls and on saving throws against fear effects.",
        "effect": "buff",
        "buff_type": "attack_save",
        "bonus": 1,
        "class": "Cleric"
    },
    "Divine Favor": {
        "name": "Divine Favor",
        "level": 1,
        "school": "Evocation",
        "subschool": "",
        "casting_time": "Standard Action",
        "range": "Personal",
        "target": "You",
        "duration": "1 minute",
        "saving_throw": "None",
        "spell_resistance": "No",
        "description": "Calling upon the strength and wisdom of a deity, you gain a +1 luck bonus on attack and weapon damage rolls for every three caster levels you have (maximum +3).",
        "effect": "buff",
        "buff_type": "attack_damage",
        "bonus": 1,
        "class": "Cleric"
    },
    
    # Wizard Spells
    "Magic Missile": {
        "name": "Magic Missile",
        "level": 1,
        "school": "Evocation",
        "subschool": "Force",
        "casting_time": "Standard Action",
        "range": "Medium (100 ft. + 10 ft./level)",
        "target": "Up to five creatures, no two of which can be more than 15 ft. apart",
        "duration": "Instantaneous",
        "saving_throw": "None",
        "spell_resistance": "Yes",
        "description": "A missile of magical energy darts forth from your fingertip and strikes its target, dealing 1d4+1 points of force damage.",
        "effect": "damage",
        "damage_amount": "1d4+1",
        "damage_type": "Force",
        "class": "Wizard"
    },
    "Burning Hands": {
        "name": "Burning Hands",
        "level": 1,
        "school": "Evocation",
        "subschool": "Fire",
        "casting_time": "Standard Action",
        "range": "15 ft.",
        "target": "Cone-shaped burst",
        "duration": "Instantaneous",
        "saving_throw": "Reflex half",
        "spell_resistance": "Yes",
        "description": "A cone of searing flame shoots from your fingertips. Any creature in the area of the flames takes 1d4 points of fire damage per caster level (maximum 5d4).",
        "effect": "damage",
        "damage_amount": "1d4",
        "damage_type": "Fire",
        "area_effect": True,
        "class": "Wizard"
    },
    "Mage Armor": {
        "name": "Mage Armor",
        "level": 1,
        "school": "Conjuration",
        "subschool": "Creation",
        "casting_time": "Standard Action",
        "range": "Touch",
        "target": "Creature touched",
        "duration": "1 hour/level (D)",
        "saving_throw": "Will negates (harmless)",
        "spell_resistance": "No",
        "description": "An invisible but tangible field of force surrounds the subject of a mage armor spell, providing a +4 armor bonus to AC.",
        "effect": "buff",
        "buff_type": "armor_class",
        "bonus": 4,
        "class": "Wizard"
    },
    "Sleep": {
        "name": "Sleep",
        "level": 1,
        "school": "Enchantment",
        "subschool": "Compulsion",
        "casting_time": "Standard Action",
        "range": "Medium (100 ft. + 10 ft./level)",
        "target": "One or more living creatures within a 10-ft.-radius burst",
        "duration": "1 min./level",
        "saving_throw": "Will negates",
        "spell_resistance": "Yes",
        "description": "A sleep spell causes a magical slumber to come upon 4 Hit Dice of creatures. Creatures with the fewest HD are affected first.",
        "effect": "status",
        "status_type": "sleep",
        "duration": "1 min/level",
        "class": "Wizard"
    }
}

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
    
    # Check if character can cast this spell
    character_class = character["class"]
    if spell["class"] != character_class:
        return False, f"You cannot cast {spell_name} as a {character_class}", None
    
    # Check spell level
    spell_level = spell["level"]
    spell_slots = calculate_spell_slots(character)
    
    if str(spell_level) not in spell_slots or spell_slots[str(spell_level)] <= 0:
        return False, f"You have no spell slots of level {spell_level} remaining", None
    
    # Cast the spell
    effect_value = None
    message = f"{character['name']} casts {spell_name}!"
    
    if spell["effect"] == "heal":
        if target is None:
            target = character  # Self-heal if no target specified
        
        heal_amount = roll_dice(spell["heal_amount"])
        effect_value = heal_amount
        message += f" {target['name']} is healed for {heal_amount} hit points."
        
        # Apply healing
        old_hp = target["current_hp"]
        target["current_hp"] = min(target["max_hp"], target["current_hp"] + heal_amount)
        actual_heal = target["current_hp"] - old_hp
        if actual_heal < heal_amount:
            message += f" (Maximum HP reached)"
    
    elif spell["effect"] == "damage":
        if target is None:
            return False, f"{spell_name} requires a target", None
        
        damage_amount = roll_dice(spell["damage_amount"])
        effect_value = damage_amount
        message += f" {target['name']} takes {damage_amount} {spell['damage_type']} damage."
        
        # Apply damage
        target["current_hp"] = max(0, target["current_hp"] - damage_amount)
    
    elif spell["effect"] == "buff":
        if target is None:
            target = character  # Self-buff if no target specified
        
        bonus = spell["bonus"]
        effect_value = bonus
        buff_type = spell["buff_type"]
        
        if buff_type == "attack_damage":
            message += f" {target['name']} gains +{bonus} to attack and damage rolls."
        elif buff_type == "armor_class":
            message += f" {target['name']} gains +{bonus} to Armor Class."
        elif buff_type == "attack_save":
            message += f" {target['name']} gains +{bonus} to attack rolls and saves vs fear."
    
    elif spell["effect"] == "status":
        if target is None:
            return False, f"{spell_name} requires a target", None
        
        status_type = spell["status_type"]
        if status_type == "sleep":
            message += f" {target['name']} falls asleep!"
            # In a full implementation, you'd track status effects
            # For now, we'll just apply some damage to represent the effect
            damage = roll_dice("1d4")
            target["current_hp"] = max(0, target["current_hp"] - damage)
            message += f" {target['name']} takes {damage} damage from the magical sleep."
    
    # Consume spell slot
    spell_slots[str(spell_level)] -= 1
    
    return True, message, effect_value

def display_spell_list(character: Dict[str, Any]):
    """Display all spells available to the character"""
    available_spells = get_available_spells(character)
    spell_slots = calculate_spell_slots(character)
    
    console.print(f"\n[bold cyan]Spell List - {character['name']} (Level {character['level']} {character['class']})[/bold cyan]")
    
    for spell_level in sorted(available_spells.keys(), key=int):
        level_name = "Cantrips" if spell_level == "0" else f"Level {spell_level}"
        slots = spell_slots.get(spell_level, 0)
        
        console.print(f"\n[bold yellow]{level_name} ({slots} slots):[/bold yellow]")
        
        if available_spells[spell_level]:
            for spell_name in available_spells[spell_level]:
                spell = SPELLS[spell_name]
                console.print(f"  [cyan]{spell_name}[/cyan] - {spell['description'][:60]}...")
        else:
            console.print("  [dim]No spells available[/dim]")

def select_spell_to_cast(character: Dict[str, Any]) -> Optional[str]:
    """Let the player select a spell to cast"""
    available_spells = get_available_spells(character)
    spell_slots = calculate_spell_slots(character)
    
    # Flatten all available spells into a list
    all_spells = []
    for spell_level in sorted(available_spells.keys(), key=int):
        level_name = "Cantrips" if spell_level == "0" else f"Level {spell_level}"
        slots = spell_slots.get(spell_level, 0)
        
        for spell_name in available_spells[spell_level]:
            spell = SPELLS[spell_name]
            all_spells.append(f"{spell_name} ({level_name}, {slots} slots) - {spell['description'][:40]}...")
    
    if not all_spells:
        console.print("[yellow]You have no spells available to cast.[/yellow]")
        return None
    
    # Add "Cancel" option
    all_spells.append("Cancel")
    
    choice = print_choice_menu(all_spells, "Select a spell to cast:")
    
    if choice == len(all_spells) - 1:  # Cancel
        return None
    
    # Extract spell name from the choice
    selected_spell = all_spells[choice].split(" (")[0]
    return selected_spell

def get_spell_info(spell_name: str) -> str:
    """Get detailed information about a spell"""
    if spell_name not in SPELLS:
        return f"Unknown spell: {spell_name}"
    
    spell = SPELLS[spell_name]
    
    info = f"[bold cyan]{spell['name']}[/bold cyan]\n"
    info += f"Level: {spell['level']} {spell['class']}\n"
    info += f"School: {spell['school']}"
    if spell['subschool']:
        info += f" ({spell['subschool']})"
    info += f"\n"
    info += f"Casting Time: {spell['casting_time']}\n"
    info += f"Range: {spell['range']}\n"
    info += f"Target: {spell['target']}\n"
    info += f"Duration: {spell['duration']}\n"
    info += f"Saving Throw: {spell['saving_throw']}\n"
    info += f"Spell Resistance: {spell['spell_resistance']}\n\n"
    info += f"[italic]{spell['description']}[/italic]"
    
    return info 