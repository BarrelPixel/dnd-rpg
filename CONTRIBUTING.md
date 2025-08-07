# Contributing to D&D RPG

## Project Overview
This is a text-based D&D 3.5e RPG implementation in Python. The game features character creation, turn-based combat, and dungeon exploration.

## Project Structure
```
dnd-rpg/
├── character.py       # Character creation and management
├── combat.py         # Combat system implementation
├── command_handler.py # Handles game commands
├── config/           # Configuration files
├── data/            # Game data (classes, races, spells, etc.)
├── dungeon.py       # Dungeon generation and exploration
├── enhanced_ui.py   # Rich text UI components
├── game_state.py    # Game state management
├── main.py          # Main game loop and entry point
├── models.py        # Data models and classes
├── spells.py        # Spell system implementation
└── utils.py         # Utility functions
```

## Key Components

### Character System
- Character creation with races and classes from D&D 3.5e
- Ability scores (Strength, Dexterity, etc.)
- Level progression and experience
- Equipment and inventory management

### Combat System
- Turn-based combat following D&D 3.5e rules
- Initiative system
- Attack rolls and damage calculation
- Spell casting in combat

### Dungeon System
- Procedural dungeon generation
- Room exploration
- Monster encounters
- Treasure and loot

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and returns
- Document classes and functions with docstrings

### Adding New Features
1. Create a new branch for your feature
2. Implement the feature with appropriate tests
3. Update documentation
4. Submit a pull request

### Testing
- Write unit tests for new features
- Run existing tests before submitting changes
- Ensure all tests pass before committing

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python main.py`

## Need Help?
- Check existing documentation in the `/docs` directory
- Review the codebase and comments
- Reach out to project maintainers