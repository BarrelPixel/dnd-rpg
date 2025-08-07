# D&D 3.5e RPG - AI Dungeon Master

An interactive text-based D&D 3.5e roleplaying game powered by OpenAI's GPT API. Experience dynamic storytelling with an AI Dungeon Master that adapts to your choices and follows D&D 3.5e rules.

## 🎲 Features

- **AI Dungeon Master**: OpenAI-powered storytelling that adapts to player choices
- **D&D 3.5e Rules**: Full implementation of D&D 3.5e mechanics and systems
- **Interactive Storytelling**: Dynamic narrative that responds to player actions
- **Character Creation**: Complete character creation with races, classes, and abilities
- **Combat System**: Turn-based combat following D&D 3.5e rules
- **Spell System**: Comprehensive spellcasting with D&D 3.5e spells
- **Procedural Content**: AI-generated encounters, NPCs, and story elements

## 🏗️ Project Structure

```
dnd35-rpg/
├── main.py              # Main game loop and entry point
├── models.py            # Data models and structures
├── utils.py             # Utility functions and dice rolling
├── game_state.py        # Game state management
├── ai_dm.py             # AI Dungeon Master implementation
├── character.py         # Character creation and management
├── combat.py            # Combat system implementation
├── spells.py            # Spell system and casting
├── data/                # Game data files
│   ├── classes.json     # D&D 3.5e classes
│   ├── races.json       # D&D 3.5e races
│   ├── spells.json      # D&D 3.5e spells
│   └── monsters.json    # D&D 3.5e monsters
└── config/              # Configuration files
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/BarrelPixel/dnd35-rpg.git
cd dnd35-rpg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the game:
```bash
python main.py
```

## 🎮 How It Works

1. **Character Creation**: Create your hero using D&D 3.5e rules
2. **AI Dungeon Master**: The AI creates dynamic scenarios and responds to your choices
3. **Interactive Story**: Every decision you make shapes the narrative
4. **D&D 3.5e Mechanics**: All gameplay follows official D&D 3.5e rules
5. **Procedural Content**: AI generates unique encounters, NPCs, and story elements

## 🔧 Development

This project combines:
- **D&D 3.5e Rules Engine**: Accurate implementation of tabletop mechanics
- **OpenAI GPT Integration**: AI-powered storytelling and content generation
- **Interactive Fiction**: Dynamic narrative that adapts to player choices
- **Procedural Generation**: AI-created content for endless replayability

### Key Components

- **AI Dungeon Master**: Handles storytelling, NPC interactions, and world-building
- **Rules Engine**: Implements D&D 3.5e mechanics (combat, spells, skills)
- **Character System**: Complete character creation and progression
- **Story Engine**: Manages narrative flow and player choices

## 📝 License

This project is for educational and entertainment purposes. D&D is a trademark of Wizards of the Coast.