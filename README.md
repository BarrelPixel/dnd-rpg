# D&D 3.5e Text-Based RPG

A text-based role-playing game based on Dungeons & Dragons 3.5e rules, featuring an AI Dungeon Master that guides you through exciting adventures!

## Features

- **Character Creation**: Create and customize your D&D 3.5e character
- **AI Dungeon Master**: Intelligent AI that narrates and manages your adventure
- **Combat System**: Turn-based combat with initiative, attacks, and damage calculation
- **Dungeon Generation**: Procedurally generated dungeons and encounters
- **Rich Text Interface**: Beautiful console-based UI with colors and formatting

## Setup Instructions

1. **Install Python**: Make sure you have Python 3.8+ installed
2. **Install Dependencies**: Run `pip install -r requirements.txt`
3. **Set up OpenAI API**: 
   - Get an API key from [OpenAI](https://platform.openai.com/)
   - Create a `.env` file in the project root
   - Add: `OPENAI_API_KEY=your_api_key_here`
4. **Run the Game**: Execute `python main.py`

## How to Play

1. Start the game and create your character
2. The AI Dungeon Master will introduce your adventure
3. Navigate through the dungeon using text commands
4. Engage in combat when you encounter enemies
5. Complete quests and level up your character

## Game Commands

- `look` - Examine your surroundings
- `move [direction]` - Move in a direction (north, south, east, west)
- `attack [target]` - Attack an enemy
- `cast [spell]` - Cast a spell (if you're a spellcaster)
- `inventory` - Check your inventory
- `character` - View character sheet
- `help` - Show available commands
- `quit` - Exit the game

## Project Structure

```
dnd-rpg/
├── main.py              # Main game entry point
├── character.py         # Character creation and management
├── combat.py           # Combat system
├── dungeon_master.py   # AI Dungeon Master
├── dungeon.py          # Dungeon generation and navigation
├── game_state.py       # Game state management
├── utils.py            # Utility functions
└── requirements.txt    # Python dependencies
```

## Learning Resources

This project demonstrates:
- Object-oriented programming
- Game state management
- API integration
- Text parsing and user input
- Random number generation
- File I/O and data persistence

Perfect for learning Python programming concepts while having fun with D&D! 