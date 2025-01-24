from .. import pygame
from .key_utils import create_key_tracking_dict


class GameState:
    def __init__(self, screen: pygame.Surface):
        # run flag
        self.running = True
        
        # pygame internals
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.events = list[pygame.event.Event]()

        # key tracking
        self.keys_pressed = create_key_tracking_dict()
        self.keys_down = create_key_tracking_dict()
        self.keys_up = create_key_tracking_dict()

        # unescaled timer
        self.unscaled_current_ticks = 0
        self.unescaled_delta_ticks = 0

        # main timer
        self.current_ticks = 0
        self.delta_ticks = 0
        self.current_time = 0.0
        self.delta_time = 0.0
        self.paused = False
        self.pause_started_at = 0

        # scene management
        self.current_scene_idx = 0
        self.current_scene_started = 0
        self.next_scene_idx = None
        self.previous_scene_idx = None
        self.entering_scene = True
        self.exiting_scene = False
