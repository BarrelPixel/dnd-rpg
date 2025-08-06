"""
Character creation and management for D&D 3.5e RPG
"""
import random
from typing import Dict, Any, List
from utils import (
    roll_ability_score, calculate_modifier, print_choice_menu, 
    print_character_sheet, console, Prompt
)

# D&D 3.5e Races
RACES = {
    "Human": {
        "description": "Versatile and adaptable",
        "ability_bonuses": {"all": 1},
        "traits": ["Bonus feat", "Extra skill points"]
    },
    "Elf": {
        "description": "Graceful and magical",
        "ability_bonuses": {"dexterity": 2, "constitution": -2},
        "traits": ["Low-light vision", "Elven weapon familiarity", "Immunity to sleep"]
    },
    "Dwarf": {
        "description": "Sturdy and determined",
        "ability_bonuses": {"constitution": 2, "charisma": -2},
        "traits": ["Darkvision", "Stonecunning", "Stability"]
    },
    "Halfling": {
        "description": "Small and nimble",
        "ability_bonuses": {"dexterity": 2, "strength": -2},
        "traits": ["Small size", "Fearless", "Lucky"]
    }
}

# D&D 3.5e Classes
CLASSES = {
    "Fighter": {
        "description": "Master of martial combat",
        "hit_die": 10,
        "base_attack_bonus": "Good",
        "saves": {"fortitude": "Good", "reflex": "Poor", "will": "Poor"},
        "skills_per_level": 2,
        "class_features": ["Bonus feats", "Weapon specialization"]
    },
    "Wizard": {
        "description": "Master of arcane magic",
        "hit_die": 4,
        "base_attack_bonus": "Poor",
        "saves": {"fortitude": "Poor", "reflex": "Poor", "will": "Good"},
        "skills_per_level": 2,
        "class_features": ["Spellcasting", "Arcane bond", "School specialization"]
    },
    "Cleric": {
        "description": "Divine spellcaster and healer",
        "hit_die": 8,
        "base_attack_bonus": "Average",
        "saves": {"fortitude": "Good", "reflex": "Poor", "will": "Good"},
        "skills_per_level": 2,
        "class_features": ["Spellcasting", "Turn undead", "Domain powers"]
    },
    "Rogue": {
        "description": "Skilled and stealthy",
        "hit_die": 6,
        "base_attack_bonus": "Average",
        "saves": {"fortitude": "Poor", "reflex": "Good", "will": "Poor"},
        "skills_per_level": 8,
        "class_features": ["Sneak attack", "Trapfinding", "Evasion"]
    }
}

# Starting equipment by class
STARTING_EQUIPMENT = {
    "Fighter": {
        "weapons": ["Longsword", "Shortbow"],
        "armor": "Chain shirt",
        "gear": ["Backpack", "Bedroll", "Rations (5 days)", "Waterskin", "50 ft rope"]
    },
    "Wizard": {
        "weapons": ["Quarterstaff"],
        "armor": "None",
        "gear": ["Spellbook", "Component pouch", "Backpack", "Bedroll", "Rations (5 days)", "Waterskin"]
    },
    "Cleric": {
        "weapons": ["Mace", "Crossbow, light"],
        "armor": "Scale mail",
        "gear": ["Holy symbol", "Backpack", "Bedroll", "Rations (5 days)", "Waterskin"]
    },
    "Rogue": {
        "weapons": ["Short sword", "Shortbow"],
        "armor": "Leather armor",
        "gear": ["Thieves' tools", "Backpack", "Bedroll", "Rations (5 days)", "Waterskin", "50 ft rope"]
    }
}

def create_character() -> Dict[str, Any]:
    """Create a new D&D 3.5e character"""
    console.print("\n[bold green]Character Creation[/bold green]")
    console.print("Let's create your hero!\n")
    
    # Get character name
    name = Prompt.ask("Enter your character's name")
    
    # Choose race
    race_options = list(RACES.keys())
    race_index = print_choice_menu(race_options, "Choose your race:")
    race = race_options[race_index]
    
    console.print(f"\n[green]Selected race: {race}[/green]")
    console.print(f"[italic]{RACES[race]['description']}[/italic]")
    
    # Choose class
    class_options = list(CLASSES.keys())
    class_index = print_choice_menu(class_options, "Choose your class:")
    character_class = class_options[class_index]
    
    console.print(f"\n[green]Selected class: {character_class}[/green]")
    console.print(f"[italic]{CLASSES[character_class]['description']}[/italic]")
    
    # Roll ability scores
    console.print("\n[bold yellow]Rolling Ability Scores[/bold yellow]")
    console.print("Rolling 4d6, dropping the lowest...")
    
    abilities = {}
    ability_names = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
    
    for ability in ability_names:
        score = roll_ability_score()
        abilities[ability] = score
        modifier = calculate_modifier(score)
        modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
        console.print(f"{ability.title()}: {score} ({modifier_str})")
    
    # Apply racial bonuses
    race_data = RACES[race]
    for ability, bonus in race_data.get("ability_bonuses", {}).items():
        if ability == "all":
            for abil in abilities:
                abilities[abil] += bonus
        else:
            abilities[ability] += bonus
    
    console.print(f"\n[green]After racial bonuses:[/green]")
    for ability in ability_names:
        score = abilities[ability]
        modifier = calculate_modifier(score)
        modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
        console.print(f"{ability.title()}: {score} ({modifier_str})")
    
    # Calculate derived stats
    class_data = CLASSES[character_class]
    
    # Hit Points
    con_modifier = calculate_modifier(abilities['constitution'])
    max_hp = class_data['hit_die'] + con_modifier
    max_hp = max(1, max_hp)  # Minimum 1 HP
    
    # Armor Class
    dex_modifier = calculate_modifier(abilities['dexterity'])
    armor_class = 10 + dex_modifier
    
    # Initiative
    initiative_bonus = dex_modifier
    
    # Create character dictionary
    character = {
        'name': name,
        'race': race,
        'class': character_class,
        'level': 1,
        'abilities': abilities,
        'max_hp': max_hp,
        'current_hp': max_hp,
        'armor_class': armor_class,
        'initiative_bonus': initiative_bonus,
        'experience': 0,
        'inventory': {},
        'equipment': get_starting_equipment(character_class),
        'spells': [] if character_class in ['Wizard', 'Cleric'] else None,
        'feats': [],
        'skills': {}
    }
    
    # Add racial traits
    character['traits'] = race_data.get('traits', [])
    
    # Add class features
    character['class_features'] = class_data.get('class_features', [])
    
    console.print(f"\n[bold green]Character created successfully![/bold green]")
    print_character_sheet(character)
    
    # Show spell information for spellcasters
    if character_class in ['Cleric', 'Wizard']:
        from spells import display_spell_list
        display_spell_list(character)
    
    return character

def get_starting_equipment(character_class: str) -> Dict[str, Any]:
    """Get starting equipment for a character class"""
    equipment = STARTING_EQUIPMENT.get(character_class, {})
    
    # Convert to inventory format
    inventory = {}
    for weapon in equipment.get('weapons', []):
        inventory[weapon] = 1
    
    if equipment.get('armor'):
        inventory[equipment['armor']] = 1
    
    for item in equipment.get('gear', []):
        inventory[item] = 1
    
    return inventory

def level_up_character(character: Dict[str, Any]) -> Dict[str, Any]:
    """Level up a character"""
    character['level'] += 1
    
    # Increase hit points
    class_data = CLASSES[character['class']]
    con_modifier = calculate_modifier(character['abilities']['constitution'])
    hp_gain = random.randint(1, class_data['hit_die']) + con_modifier
    hp_gain = max(1, hp_gain)  # Minimum 1 HP gain
    
    character['max_hp'] += hp_gain
    character['current_hp'] += hp_gain
    
    console.print(f"\n[bold green]Level Up![/bold green]")
    console.print(f"[green]You are now level {character['level']}![/green]")
    console.print(f"[green]Gained {hp_gain} hit points![/green]")
    
    return character

def heal_character(character: Dict[str, Any], amount: int) -> Dict[str, Any]:
    """Heal a character by the specified amount"""
    old_hp = character['current_hp']
    character['current_hp'] = min(character['max_hp'], character['current_hp'] + amount)
    healed = character['current_hp'] - old_hp
    
    if healed > 0:
        console.print(f"[green]Healed {healed} hit points![/green]")
    
    return character

def damage_character(character: Dict[str, Any], amount: int) -> Dict[str, Any]:
    """Damage a character by the specified amount"""
    character['current_hp'] = max(0, character['current_hp'] - amount)
    
    if character['current_hp'] == 0:
        console.print(f"[red]{character['name']} is unconscious![/red]")
    else:
        console.print(f"[red]{character['name']} takes {amount} damage![/red]")
    
    return character

def is_character_alive(character: Dict[str, Any]) -> bool:
    """Check if character is alive"""
    return character['current_hp'] > 0

def get_attack_bonus(character: Dict[str, Any]) -> int:
    """Calculate character's attack bonus"""
    class_data = CLASSES[character['class']]
    bab_type = class_data['base_attack_bonus']
    
    # Simplified BAB calculation
    if bab_type == "Good":
        bab = character['level']
    elif bab_type == "Average":
        bab = character['level'] * 3 // 4
    else:  # Poor
        bab = character['level'] // 2
    
    str_modifier = calculate_modifier(character['abilities']['strength'])
    return bab + str_modifier

def get_damage_bonus(character: Dict[str, Any]) -> int:
    """Calculate character's damage bonus"""
    str_modifier = calculate_modifier(character['abilities']['strength'])
    return str_modifier if str_modifier > 0 else 0 