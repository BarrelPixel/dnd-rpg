"""
Dungeon generation and navigation for D&D 3.5e RPG
"""
import random
from typing import Dict, Any, List, Optional
from utils import print_narrative, dramatic_pause, console

# Room types and their descriptions
ROOM_TYPES = {
    "entrance": {
        "name": "Dungeon Entrance",
        "description": "A dark opening in the earth, leading down into the depths. Torchlight flickers from within.",
        "encounter_chance": 0.1
    },
    "corridor": {
        "name": "Stone Corridor",
        "description": "A narrow passage carved from solid rock. The air is stale and the walls are damp with moisture.",
        "encounter_chance": 0.3
    },
    "chamber": {
        "name": "Ancient Chamber",
        "description": "A large room with high ceilings. Ancient runes are carved into the walls, and dust covers the floor.",
        "encounter_chance": 0.5
    },
    "treasure_room": {
        "name": "Treasure Chamber",
        "description": "A small room that glitters with the promise of wealth. Gold coins and precious gems are scattered about.",
        "encounter_chance": 0.7
    },
    "boss_room": {
        "name": "Throne Room",
        "description": "A grand hall with a massive throne at the far end. This is clearly the domain of a powerful being.",
        "encounter_chance": 1.0
    }
}

# Direction mappings
DIRECTIONS = {
    "north": (0, -1),
    "south": (0, 1),
    "east": (1, 0),
    "west": (-1, 0)
}

OPPOSITE_DIRECTIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east"
}

class DungeonRoom:
    """Represents a single room in the dungeon"""
    
    def __init__(self, room_type: str, x: int, y: int):
        self.room_type = room_type
        self.x = x
        self.y = y
        self.visited = False
        self.exits = {}  # direction -> (x, y) coordinates
        self.encounter = None
        self.treasure = None
        self.description = ROOM_TYPES[room_type]["description"]
        self.name = ROOM_TYPES[room_type]["name"]
    
    def add_exit(self, direction: str, target_x: int, target_y: int):
        """Add an exit to another room"""
        self.exits[direction] = (target_x, target_y)
    
    def get_available_exits(self) -> List[str]:
        """Get list of available exit directions"""
        return list(self.exits.keys())
    
    def describe_room(self) -> str:
        """Generate a description of the room"""
        if not self.visited:
            self.visited = True
            return f"You enter {self.name.lower()}. {self.description}"
        else:
            return f"You are in {self.name.lower()}. {self.description}"

class Dungeon:
    """Represents the entire dungeon"""
    
    def __init__(self, width: int = 5, height: int = 5):
        self.width = width
        self.height = height
        self.rooms = {}  # (x, y) -> DungeonRoom
        self.current_position = (0, 0)
        self.entrance = (0, 0)
        self.boss_room = None
        self.generate_dungeon()
    
    def generate_dungeon(self):
        """Generate a complete dungeon layout"""
        # Start with entrance
        entrance_room = DungeonRoom("entrance", 0, 0)
        self.rooms[(0, 0)] = entrance_room
        
        # Generate rooms using a simple algorithm
        self._generate_rooms_recursive(0, 0, 0, max_rooms=15)
        
        # Place boss room at the farthest point
        self._place_boss_room()
        
        # Add treasure rooms
        self._add_treasure_rooms()
        
        # Connect rooms
        self._connect_rooms()
    
    def _generate_rooms_recursive(self, x: int, y: int, depth: int, max_rooms: int):
        """Recursively generate rooms"""
        if depth >= max_rooms or len(self.rooms) >= max_rooms:
            return
        
        # Try to add rooms in each direction
        directions = list(DIRECTIONS.keys())
        random.shuffle(directions)
        
        for direction in directions:
            if random.random() < 0.7:  # 70% chance to add a room
                dx, dy = DIRECTIONS[direction]
                new_x, new_y = x + dx, y + dy
                
                # Check bounds
                if (new_x, new_y) not in self.rooms and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    # Choose room type based on depth
                    if depth < 3:
                        room_type = "corridor"
                    elif depth < 8:
                        room_type = random.choice(["corridor", "chamber"])
                    else:
                        room_type = random.choice(["chamber", "treasure_room"])
                    
                    new_room = DungeonRoom(room_type, new_x, new_y)
                    self.rooms[(new_x, new_y)] = new_room
                    
                    # Recursively generate from this room
                    self._generate_rooms_recursive(new_x, new_y, depth + 1, max_rooms)
    
    def _place_boss_room(self):
        """Place the boss room at the farthest point from entrance"""
        if len(self.rooms) < 2:
            return
        
        # Find the room farthest from entrance
        max_distance = 0
        farthest_room = None
        
        for (x, y), room in self.rooms.items():
            if (x, y) == self.entrance:
                continue
            
            distance = abs(x) + abs(y)  # Manhattan distance
            if distance > max_distance:
                max_distance = distance
                farthest_room = (x, y)
        
        if farthest_room:
            # Replace the farthest room with a boss room
            x, y = farthest_room
            boss_room = DungeonRoom("boss_room", x, y)
            self.rooms[(x, y)] = boss_room
            self.boss_room = (x, y)
    
    def _add_treasure_rooms(self):
        """Add some treasure rooms to the dungeon"""
        chamber_rooms = [(x, y) for (x, y), room in self.rooms.items() 
                        if room.room_type == "chamber"]
        
        # Convert some chambers to treasure rooms
        num_treasure_rooms = min(2, len(chamber_rooms) // 3)
        treasure_locations = random.sample(chamber_rooms, num_treasure_rooms)
        
        for x, y in treasure_locations:
            treasure_room = DungeonRoom("treasure_room", x, y)
            self.rooms[(x, y)] = treasure_room
    
    def _connect_rooms(self):
        """Connect adjacent rooms with exits"""
        for (x, y), room in self.rooms.items():
            for direction, (dx, dy) in DIRECTIONS.items():
                target_x, target_y = x + dx, y + dy
                target_pos = (target_x, target_y)
                
                if target_pos in self.rooms:
                    room.add_exit(direction, target_x, target_y)
    
    def get_current_room(self) -> DungeonRoom:
        """Get the room at the current position"""
        return self.rooms[self.current_position]
    
    def move(self, direction: str) -> bool:
        """Move in the specified direction"""
        current_room = self.get_current_room()
        
        if direction not in current_room.exits:
            console.print(f"[red]There is no exit to the {direction}.[/red]")
            return False
        
        target_x, target_y = current_room.exits[direction]
        self.current_position = (target_x, target_y)
        
        new_room = self.get_current_room()
        console.print(f"\n[green]Moving {direction}...[/green]")
        dramatic_pause(0.5)
        console.print(f"[cyan]{new_room.describe_room()}[/cyan]")
        
        return True
    
    def get_available_moves(self) -> List[str]:
        """Get available movement directions"""
        current_room = self.get_current_room()
        return current_room.get_available_exits()
    
    def is_at_boss_room(self) -> bool:
        """Check if player is at the boss room"""
        return self.current_position == self.boss_room
    
    def get_dungeon_map(self) -> str:
        """Generate a simple ASCII map of the dungeon"""
        map_str = "Dungeon Map:\n"
        map_str += "  " + " ".join(str(i) for i in range(self.width)) + "\n"
        
        for y in range(self.height):
            map_str += f"{y} "
            for x in range(self.width):
                pos = (x, y)
                if pos == self.current_position:
                    map_str += "P "  # Player
                elif pos == self.entrance:
                    map_str += "E "  # Entrance
                elif pos == self.boss_room:
                    map_str += "B "  # Boss
                elif pos in self.rooms:
                    room = self.rooms[pos]
                    if room.room_type == "treasure_room":
                        map_str += "T "  # Treasure
                    elif room.room_type == "chamber":
                        map_str += "C "  # Chamber
                    else:
                        map_str += "R "  # Room
                else:
                    map_str += ". "  # Empty
            map_str += "\n"
        
        map_str += "\nLegend: P=Player, E=Entrance, B=Boss, T=Treasure, C=Chamber, R=Room, .=Empty"
        return map_str

def create_dungeon(width: int = 5, height: int = 5) -> Dungeon:
    """Create a new dungeon"""
    console.print("[yellow]Generating dungeon...[/yellow]")
    dramatic_pause(1.0)
    
    dungeon = Dungeon(width, height)
    
    console.print("[green]Dungeon generated successfully![/green]")
    console.print(f"Created {len(dungeon.rooms)} rooms.")
    
    return dungeon

def explore_room(room: DungeonRoom, character: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Explore a room and potentially trigger an encounter"""
    if room.encounter:
        return room.encounter
    
    # Check if encounter should occur
    encounter_chance = ROOM_TYPES[room.room_type]["encounter_chance"]
    
    if random.random() < encounter_chance:
        # Create random encounter
        from combat import create_random_encounter
        enemies = create_random_encounter(character['level'])
        room.encounter = enemies
        
        console.print(f"\n[bold red]Suddenly, enemies appear![/bold red]")
        from combat import describe_encounter
        console.print(f"[red]{describe_encounter(enemies)}[/red]")
        
        return enemies
    
    # Check for treasure
    if room.room_type == "treasure_room" and not room.treasure:
        room.treasure = generate_treasure()
        console.print(f"\n[bold yellow]You find treasure![/bold yellow]")
        console.print(f"[yellow]{room.treasure['description']}[/yellow]")
        
        # Add to character inventory
        for item, quantity in room.treasure['items'].items():
            character['inventory'][item] = character['inventory'].get(item, 0) + quantity
            console.print(f"[green]Gained {quantity}x {item}[/green]")
    
    return None

def generate_treasure() -> Dict[str, Any]:
    """Generate random treasure"""
    treasure_types = [
        {
            "description": "A small chest contains gold coins and a few gems.",
            "items": {"Gold coins": random.randint(10, 50), "Gem": random.randint(1, 3)}
        },
        {
            "description": "An ornate vase holds ancient coins and jewelry.",
            "items": {"Ancient coins": random.randint(5, 20), "Jewelry": 1}
        },
        {
            "description": "A dusty shelf holds magical scrolls and potions.",
            "items": {"Scroll": random.randint(1, 3), "Potion of Healing": random.randint(1, 2)}
        },
        {
            "description": "A wooden crate contains adventuring supplies.",
            "items": {"Potion of Healing": random.randint(1, 3), "Rations": random.randint(1, 5)}
        }
    ]
    
    return random.choice(treasure_types) 