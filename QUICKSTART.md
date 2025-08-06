# Quick Start Guide

## Getting Started in 3 Easy Steps

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. (Optional) Set up AI Dungeon Master
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```
Get your API key from: https://platform.openai.com/api-keys

### 3. Start the Game
```bash
python3 main.py
```

## First Time Playing

1. **Create Your Character**
   - Choose a race (Human, Elf, Dwarf, Halfling)
   - Choose a class (Fighter, Wizard, Cleric, Rogue)
   - Roll ability scores (4d6, drop lowest)

2. **Explore the Dungeon**
   - Use `look` to examine your surroundings
   - Use `move north/south/east/west` to navigate
   - Use `map` to see the dungeon layout

3. **Fight Enemies**
   - Combat is turn-based with initiative
   - Choose your actions: Attack, Cast Spell, Use Item, or Flee
   - Defeat enemies to gain experience and treasure

4. **Complete the Adventure**
   - Find the boss room and defeat the final enemy
   - Collect treasure and gain experience along the way

## Basic Commands

- `look` - Examine your surroundings
- `move [direction]` - Move in a direction
- `character` - View your character sheet
- `inventory` - Check your inventory
- `map` - Show dungeon map
- `save` - Save your progress
- `help` - Show help
- `quit` - Exit the game

## Tips for Beginners

- **Fighters** are good for beginners - they have high HP and good combat abilities
- **Save often** using the `save` command
- **Explore thoroughly** - you might find treasure in unexpected places
- **Don't be afraid to flee** if a fight is going badly
- **Use the map** to keep track of where you've been

## Troubleshooting

**"No module named 'rich'"**
- Run: `pip3 install -r requirements.txt`

**"No OpenAI API key found"**
- This is normal! The game will work with fallback narration
- To enable AI narration, create a `.env` file with your OpenAI API key

**Game crashes or errors**
- Try running: `python3 main.py`
- Check that all dependencies are installed
- Make sure you're in the correct directory

## Learning D&D 3.5e

This game teaches you the basics of D&D 3.5e:
- **Ability Scores**: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
- **Classes**: Different character types with unique abilities
- **Combat**: Turn-based combat with initiative, attack rolls, and damage
- **Dungeon Crawling**: Exploring, finding treasure, and fighting monsters

Have fun and may your dice roll true! 🎲 