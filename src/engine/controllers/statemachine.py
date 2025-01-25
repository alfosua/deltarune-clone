from typing import Generic, TypeVar

from .base import ControllerBase
from ..game.context.game import GameContext

T = TypeVar('T')


class StateMachineController(ControllerBase, Generic[T]):
    def __init__(self, context: GameContext, initial_state: T, auto_start: bool = True):
        super(StateMachineController, self).__init__(context)
        self.previous_state = None
        self.current_state = None
        self.next_state = None
        self.current_state_entering = False
        self.current_state_entering_at = 0
        if auto_start:
            self.start_from(initial_state)

    def init_update(self):
        if self.next_state != None:
            self.previous_state = self.current_state
            self.current_state = self.next_state
            self.next_state = None
            self.current_state_entering = True
            self.current_state_entering_at = self.context.scene.get_current_ticks()

    def finish_update(self):
        self.current_state_entering = False
        self.current_state_exiting = False

    def start_from(self, starting_state: T):
        self.current_state = starting_state
        self.current_state_entering_at = self.context.scene.get_current_ticks()
        self.current_state_entering = True
        self.current_state_exiting = False
        self.next_state = None
        self.previous_state = None
    
    def exit(self):
        self.current_state_exiting = True
        self.current_state = None

    def transition_to(self, new_state: T):
        self.next_state = new_state
        self.current_state_exiting = True
    
    def is_current(self, state: T):
        return self.current_state == state

    @property
    def started_at(self):
        return self.current_state_entering_at

    @property
    def ticks_elapsed(self):
        return self.context.scene.get_current_ticks() - self.current_state_entering_at
    
    @property
    def is_entering(self):
        return self.current_state_entering
    
    @property
    def is_exiting(self):
        return self.current_state_exiting
