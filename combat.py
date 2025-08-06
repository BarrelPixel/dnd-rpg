"""
Combat system for D&D 3.5e RPG
"""
import random
from typing import List, Dict, Any, Tuple
from utils import (
    roll_dice, print_combat_status, print_narrative, dramatic_pause,
    console, print_choice_menu, Prompt
)
from character import get_attack_bonus, get_damage_bonus, damage_character, is_character_alive
from data_loader import data_loader
from config import config
from spells import SPELLS

# Get monster data from data loader
MONSTERS = data_loader.monsters

def create_monster(monster_type: str) -> Dict[str, Any]:
    """Create a monster of the specified type"""
    if monster_type not in MONSTERS:
        monster_type = random.choice(list(MONSTERS.keys()))
    
    monster_data = MONSTERS[monster_type].copy()
    monster_data['current_hp'] = monster_data['max_hp']
    
    return monster_data

def roll_initiative(character: Dict[str, Any]) -> int:
    """Roll initiative for a character"""
    return roll_dice("1d20") + character['initiative_bonus']

def determine_initiative_order(combatants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Determine the order of combat based on initiative rolls"""
    initiative_rolls = []
    
    for combatant in combatants:
        initiative = roll_initiative(combatant)
        initiative_rolls.append((initiative, combatant))
        console.print(f"{combatant['name']} initiative: {initiative}")
    
    # Sort by initiative (highest first), then by initiative bonus as tiebreaker
    initiative_rolls.sort(key=lambda x: (x[0], x[1]['initiative_bonus']), reverse=True)
    
    return [combatant for _, combatant in initiative_rolls]

def make_attack(attacker: Dict[str, Any], target: Dict[str, Any]) -> Tuple[bool, int]:
    """Make an attack roll and return (hit, damage)"""
    # Calculate attack roll
    if 'attack_bonus' in attacker:  # Monster
        attack_bonus = attacker['attack_bonus']
    else:  # Player character
        attack_bonus = get_attack_bonus(attacker)
    
    attack_roll = roll_dice("1d20") + attack_bonus
    
    console.print(f"{attacker['name']} attacks {target['name']}...")
    console.print(f"Attack roll: {attack_roll} vs AC {target['armor_class']}")
    
    # Check if hit
    if attack_roll >= target['armor_class']:
        # Calculate damage
        if 'damage' in attacker:  # Monster
            damage = roll_dice(attacker['damage']) + attacker.get('damage_bonus', 0)
        else:  # Player character - simplified weapon damage
            weapon_damage = "1d8"  # Default weapon damage
            damage = roll_dice(weapon_damage) + get_damage_bonus(attacker)
        
        console.print(f"[green]Hit![/green] Damage: {damage}")
        return True, damage
    else:
        console.print("[red]Miss![/red]")
        return False, 0

def player_turn(character: Dict[str, Any], enemies: List[Dict[str, Any]]) -> bool:
    """Handle player's turn in combat"""
    console.print(f"\n[bold cyan]Your turn, {character['name']}![/bold cyan]")
    
    # Check if any enemies are alive
    alive_enemies = [e for e in enemies if is_character_alive(e)]
    if not alive_enemies:
        return True  # Combat is over
    
    # Show available actions
    actions = ["Attack", "Cast Spell", "Use Item", "Flee"]
    action_index = print_choice_menu(actions, "What would you like to do?")
    
    if action_index == 0:  # Attack
        # Choose target
        target_options = [f"{e['name']} (HP: {e['current_hp']}/{e['max_hp']})" for e in alive_enemies]
        target_index = print_choice_menu(target_options, "Choose your target:")
        target = alive_enemies[target_index]
        
        hit, damage = make_attack(character, target)
        if hit:
            damage_character(target, damage)
    
    elif action_index == 1:  # Cast Spell
        from spells import select_spell_to_cast, cast_spell
        
        # Select spell to cast
        spell_name = select_spell_to_cast(character)
        if spell_name is None:
            console.print("[yellow]Spellcasting cancelled. You attack instead.[/yellow]")
            # Fall back to attack
            target = alive_enemies[0]
            hit, damage = make_attack(character, target)
            if hit:
                damage_character(target, damage)
            return False
        
        # Determine target
        spell = SPELLS[spell_name]
        target = None
        
        if spell["effect"] == "heal":
            # Healing spell - can target self or allies
            target_options = [character['name']] + [e['name'] for e in alive_enemies]
            target_choice = print_choice_menu(target_options, "Choose target:")
            if target_choice == 0:
                target = character
            else:
                target = alive_enemies[target_choice - 1]
        elif spell["effect"] in ["damage", "status"]:
            # Offensive spell - must target enemy
            target_options = [f"{e['name']} (HP: {e['current_hp']}/{e['max_hp']})" for e in alive_enemies]
            target_index = print_choice_menu(target_options, "Choose your target:")
            target = alive_enemies[target_index]
        else:
            # Buff spell - usually targets self
            target = character
        
        # Cast the spell
        success, message, effect_value = cast_spell(character, spell_name, target)
        console.print(f"[magenta]{message}[/magenta]")
        
        if not success:
            console.print("[red]Spell failed! You attack instead.[/red]")
            # Fall back to attack
            target = alive_enemies[0]
            hit, damage = make_attack(character, target)
            if hit:
                damage_character(target, damage)
    
    elif action_index == 2:  # Use Item
        # Check for usable items
        usable_items = []
        for item, quantity in character.get('inventory', {}).items():
            if item == "Potion of Healing" and quantity > 0:
                usable_items.append(f"{item} ({quantity} remaining)")
        
        if not usable_items:
            console.print("[yellow]No usable items found. You attack instead.[/yellow]")
            # Fall back to attack
            target = alive_enemies[0]
            hit, damage = make_attack(character, target)
            if hit:
                damage_character(target, damage)
        else:
            # Add "Cancel" option
            usable_items.append("Cancel")
            item_choice = print_choice_menu(usable_items, "Choose an item to use:")
            
            if item_choice == len(usable_items) - 1:  # Cancel
                console.print("[yellow]Item usage cancelled. You attack instead.[/yellow]")
                # Fall back to attack
                target = alive_enemies[0]
                hit, damage = make_attack(character, target)
                if hit:
                    damage_character(target, damage)
            else:
                # Use the selected item
                selected_item = usable_items[item_choice].split(" (")[0]
                
                if selected_item == "Potion of Healing":
                    # Use healing potion
                    heal_amount = roll_dice("2d4+2")  # Standard D&D healing potion
                    old_hp = character["current_hp"]
                    character["current_hp"] = min(character["max_hp"], character["current_hp"] + heal_amount)
                    actual_heal = character["current_hp"] - old_hp
                    
                    console.print(f"[green]{character['name']} drinks a Potion of Healing and recovers {actual_heal} hit points![/green]")
                    
                    # Remove potion from inventory
                    character["inventory"]["Potion of Healing"] -= 1
                    if character["inventory"]["Potion of Healing"] <= 0:
                        del character["inventory"]["Potion of Healing"]
    
    elif action_index == 3:  # Flee
        flee_roll = roll_dice("1d20")
        if flee_roll >= 10:  # Simple flee check
            console.print("[green]You successfully flee from combat![/green]")
            return True  # End combat
        else:
            console.print("[red]You fail to flee and lose your turn![/red]")
    
    return False  # Combat continues

def monster_turn(monster: Dict[str, Any], character: Dict[str, Any]) -> bool:
    """Handle monster's turn in combat"""
    console.print(f"\n[bold red]{monster['name']}'s turn![/bold red]")
    
    if not is_character_alive(character):
        return True  # Combat is over
    
    # Simple AI: always attack
    hit, damage = make_attack(monster, character)
    if hit:
        damage_character(character, damage)
    
    return False  # Combat continues

def start_combat(character: Dict[str, Any], enemies: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Start and run a combat encounter"""
    console.print("\n[bold red]Combat begins![/bold red]")
    
    # Add character to combatants list
    combatants = [character] + enemies
    
    # Roll initiative
    console.print("\n[bold yellow]Rolling initiative...[/bold yellow]")
    initiative_order = determine_initiative_order(combatants)
    
    # Combat loop
    round_num = 1
    while True:
        console.print(f"\n[bold cyan]=== Round {round_num} ===[/bold cyan]")
        print_combat_status(combatants)
        
        # Check if combat should end
        alive_players = [c for c in combatants if c == character and is_character_alive(c)]
        alive_enemies = [c for c in combatants if c != character and is_character_alive(c)]
        
        if not alive_players:
            console.print("[red]You have been defeated![/red]")
            return character
        
        if not alive_enemies:
            console.print("[green]Victory! All enemies defeated![/green]")
            # Award XP
            total_xp = sum(e.get('xp_value', 0) for e in enemies)
            character['experience'] += total_xp
            console.print(f"[green]Gained {total_xp} experience points![/green]")
            return character
        
        # Process turns in initiative order
        for combatant in initiative_order:
            if not is_character_alive(combatant):
                continue
            
            if combatant == character:
                # Player turn
                if player_turn(character, alive_enemies):
                    return character  # Combat ended
            else:
                # Monster turn
                if monster_turn(combatant, character):
                    return character  # Combat ended
        
        round_num += 1
        dramatic_pause(0.5)

def create_random_encounter(character_level: int) -> List[Dict[str, Any]]:
    """Create a random encounter appropriate for the character's level"""
    # Get monsters appropriate for character level
    available_monsters = []
    for monster_name, monster_data in MONSTERS.items():
        if monster_data.get('level', 1) <= character_level + 1:
            available_monsters.append(monster_name)
    
    if not available_monsters:
        available_monsters = list(MONSTERS.keys())
    
    # Determine number of enemies based on character level
    if character_level <= 2:
        num_enemies = random.randint(1, 2)
    else:
        num_enemies = random.randint(1, 3)
    
    enemies = []
    for _ in range(num_enemies):
        monster_type = random.choice(available_monsters)
        enemy = create_monster(monster_type)
        enemies.append(enemy)
    
    return enemies

def describe_encounter(enemies: List[Dict[str, Any]]) -> str:
    """Generate a description of the encounter"""
    if len(enemies) == 1:
        enemy = enemies[0]
        return f"You encounter a {enemy['name'].lower()}! {enemy['description']}"
    else:
        monster_types = {}
        for enemy in enemies:
            monster_types[enemy['name']] = monster_types.get(enemy['name'], 0) + 1
        
        descriptions = []
        for monster_name, count in monster_types.items():
            if count == 1:
                descriptions.append(f"a {monster_name.lower()}")
            else:
                descriptions.append(f"{count} {monster_name.lower()}s")
        
        return f"You encounter {' and '.join(descriptions)}!" 