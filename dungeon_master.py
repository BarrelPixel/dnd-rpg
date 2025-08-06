"""
AI Dungeon Master for D&D 3.5e RPG
"""
import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from utils import console, print_narrative, dramatic_pause, print_info

class DungeonMaster:
    """AI Dungeon Master that narrates and manages the adventure"""
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            console.print("[yellow]Warning: No OpenAI API key found. Using fallback narration.[/yellow]")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.adventure_context = {
            "theme": "dark fantasy",
            "setting": "ancient dungeon",
            "tone": "epic and mysterious"
        }
    
    def generate_narration(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate AI narration using OpenAI"""
        if not self.client:
            return self._fallback_narration(prompt)
        
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt(prompt, context)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a skilled Dungeon Master for a D&D 3.5e game. 
                        Create vivid, atmospheric descriptions that immerse players in the adventure. 
                        Keep responses concise (2-3 sentences) and focus on sensory details and mood. 
                        Use dramatic language appropriate for fantasy role-playing."""
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            console.print(f"[yellow]AI narration failed: {e}. Using fallback.[/yellow]")
            return self._fallback_narration(prompt)
    
    def _build_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Build a complete prompt with context"""
        context_str = ""
        if context:
            context_str = f"\nContext: {json.dumps(context, indent=2)}"
        
        return f"""Create a vivid D&D 3.5e narration for the following situation:

{self.adventure_context['theme']} theme, {self.adventure_context['setting']} setting, {self.adventure_context['tone']} tone.

Situation: {prompt}{context_str}

Provide a brief, atmospheric description:"""
    
    def _fallback_narration(self, prompt: str) -> str:
        """Provide fallback narration when AI is unavailable"""
        fallback_responses = {
            "entrance": "The ancient stone doorway looms before you, its weathered surface covered in mysterious runes that seem to pulse with an otherworldly energy.",
            "combat": "The air crackles with tension as steel meets steel, and the sound of battle echoes through the dungeon corridors.",
            "treasure": "A glint of gold catches your eye, revealing treasures that have lain undisturbed for centuries.",
            "victory": "The last enemy falls, and a sense of triumph washes over you as you stand victorious in the aftermath of battle.",
            "defeat": "Darkness closes in as your strength fails, and you feel the cold embrace of unconsciousness.",
            "exploration": "You carefully explore the chamber, your footsteps echoing softly against the ancient stone walls.",
            "boss": "A powerful presence fills the room, and you know you face a challenge unlike any you've encountered before."
        }
        
        # Find the best matching fallback
        for key, response in fallback_responses.items():
            if key in prompt.lower():
                return response
        
        return "The adventure continues as you press deeper into the dungeon's mysteries."
    
    def introduce_adventure(self, character: Dict[str, Any]) -> str:
        """Introduce the adventure to the player"""
        context = {
            "character_name": character['name'],
            "character_class": character['class'],
            "character_race": character['race']
        }
        
        prompt = f"Introduce a D&D adventure where {character['name']}, a {character['race']} {character['class']}, enters an ancient dungeon to seek treasure and glory."
        
        narration = self.generate_narration(prompt, context)
        
        print_narrative(f"\n[bold cyan]The Dungeon Master speaks:[/bold cyan]")
        print_narrative(narration, "cyan")
        dramatic_pause(1.0)
        
        return narration
    
    def describe_room_entrance(self, room_type: str, character: Dict[str, Any]) -> str:
        """Describe entering a new room"""
        context = {
            "room_type": room_type,
            "character_name": character['name']
        }
        
        prompt = f"Describe {character['name']} entering a {room_type} in the dungeon."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "cyan")
        
        return narration
    
    def describe_combat_start(self, enemies: List[Dict[str, Any]], character: Dict[str, Any]) -> str:
        """Describe the start of combat"""
        enemy_names = [enemy['name'] for enemy in enemies]
        context = {
            "enemies": enemy_names,
            "character_name": character['name']
        }
        
        prompt = f"Describe the start of combat between {character['name']} and {', '.join(enemy_names)}."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "red")
        
        return narration
    
    def describe_combat_action(self, attacker: Dict[str, Any], target: Dict[str, Any], hit: bool, damage: int = 0) -> str:
        """Describe a combat action"""
        context = {
            "attacker": attacker['name'],
            "target": target['name'],
            "hit": hit,
            "damage": damage
        }
        
        if hit:
            prompt = f"Describe {attacker['name']} successfully hitting {target['name']} for {damage} damage."
        else:
            prompt = f"Describe {attacker['name']} missing {target['name']} with their attack."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "yellow")
        
        return narration
    
    def describe_victory(self, character: Dict[str, Any], enemies: List[Dict[str, Any]]) -> str:
        """Describe victory in combat"""
        context = {
            "character_name": character['name'],
            "enemies_defeated": [enemy['name'] for enemy in enemies]
        }
        
        prompt = f"Describe {character['name']} achieving victory over the defeated enemies."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "green")
        
        return narration
    
    def describe_defeat(self, character: Dict[str, Any]) -> str:
        """Describe defeat in combat"""
        context = {
            "character_name": character['name']
        }
        
        prompt = f"Describe {character['name']} being defeated in combat."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "red")
        
        return narration
    
    def describe_treasure_find(self, character: Dict[str, Any], treasure: Dict[str, Any]) -> str:
        """Describe finding treasure"""
        context = {
            "character_name": character['name'],
            "treasure_description": treasure['description']
        }
        
        prompt = f"Describe {character['name']} discovering treasure: {treasure['description']}"
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "yellow")
        
        return narration
    
    def describe_boss_encounter(self, character: Dict[str, Any]) -> str:
        """Describe encountering the boss"""
        context = {
            "character_name": character['name']
        }
        
        prompt = f"Describe {character['name']} entering the boss room and encountering the dungeon's master."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "red")
        
        return narration
    
    def describe_adventure_end(self, character: Dict[str, Any], victory: bool) -> str:
        """Describe the end of the adventure"""
        context = {
            "character_name": character['name'],
            "victory": victory
        }
        
        if victory:
            prompt = f"Describe {character['name']} successfully completing the dungeon adventure and emerging victorious."
        else:
            prompt = f"Describe {character['name']} being defeated and the adventure ending in failure."
        
        narration = self.generate_narration(prompt, context)
        print_narrative(narration, "cyan")
        
        return narration
    
    def provide_hint(self, situation: str, character: Dict[str, Any]) -> str:
        """Provide a helpful hint to the player"""
        context = {
            "character_name": character['name'],
            "situation": situation
        }
        
        prompt = f"Provide a helpful hint to {character['name']} about the current situation: {situation}"
        
        narration = self.generate_narration(prompt, context)
        print_narrative(f"[italic]Hint: {narration}[/italic]", "blue")
        
        return narration
    
    def set_adventure_theme(self, theme: str, setting: str, tone: str):
        """Set the adventure's theme, setting, and tone"""
        self.adventure_context = {
            "theme": theme,
            "setting": setting,
            "tone": tone
        }
        
        print_info(f"Adventure theme set to: {theme} in {setting} with {tone} tone") 