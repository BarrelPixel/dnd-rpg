"""
Utility functions for D&D RPG game
"""
import random
from typing import List, Tuple

def roll_dice(num_dice: int, sides: int) -> int:
    """Roll any number of dice with given sides"""
    return sum(random.randint(1, sides) for _ in range(num_dice))

def roll_ability_score() -> int:
    """Roll 4d6 drop lowest for ability scores"""
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls)[1:])  # Drop lowest roll

def calculate_modifier(score: int) -> int:
    """Calculate ability modifier from score"""
    return (score - 10) // 2

def roll_attack(bonus: int) -> Tuple[int, bool]:
    """
    Roll attack with bonus, return total and if critical
    """
    roll = random.randint(1, 20)
    is_crit = roll == 20
    return roll + bonus, is_crit

def roll_damage(damage_dice: str, bonus: int = 0) -> int:
    """
    Roll damage based on damage dice string (e.g. '2d6+2')
    """
    # Strip any whitespace and plus sign
    dice_str = damage_dice.replace(' ', '').replace('+', '')
    
    # Split into number of dice and sides
    num_dice, sides = map(int, dice_str.lower().split('d'))
    
    return roll_dice(num_dice, sides) + bonus