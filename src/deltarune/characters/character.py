from engine import *
from .action import CharacterAction


class Character:
    def __init__(self,
                 name: str,
                 max_hp: int,
                 current_hp: int,
                 primary_color: Color,
                 actions: list[CharacterAction]):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.primary_color = primary_color
        self.actions = actions
