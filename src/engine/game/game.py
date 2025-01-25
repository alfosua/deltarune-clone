from .. import pygame

from .key_utils import create_key_tracking_dict
from .setup import GameSetup
from .state import GameState
from .context.game import GameContext

class Game:
    def __init__(self, setup: GameSetup):
        self.setup = setup

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
    
    def init_screen(self):
        screen = pygame.display.set_mode((1280, 960))
        pygame.display.set_caption(self.setup.title)
        return screen
    
    def init_frame(self, state: GameState):
        # capture information for the timers
        state.unescaled_delta_ticks = pygame.time.get_ticks() - state.unscaled_current_ticks
        state.unscaled_current_ticks = pygame.time.get_ticks()
        if not state.paused:
            state.delta_ticks = state.unescaled_delta_ticks
            state.current_ticks = state.current_ticks + state.delta_ticks
            state.delta_time = state.delta_ticks / 1000
            state.current_time = state.current_ticks / 1000
            state.pause_started_at = 0
        else:
            state.delta_ticks = 0
            state.delta_time = 0
            if not state.pause_started_at:
                state.pause_started_at = state.unscaled_current_ticks

        # initialize key tracking for the given grame
        state.keys_pressed = pygame.key.get_pressed()
        state.keys_down = create_key_tracking_dict()
        state.keys_up = create_key_tracking_dict()

        # process events initially for basic logical captures
        state.events = pygame.event.get()
        for event in state.events:
            if event.type == pygame.QUIT:
                state.running = False
            if event.type == pygame.KEYDOWN:
                state.keys_down[event.key] = True
            if event.type == pygame.KEYUP:
                state.keys_up[event.key] = True

        # scene management initialization per frame
        if state.next_scene_idx != None:
            state.previous_scene_idx = state.current_scene_idx
            state.current_scene_idx = state.next_scene_idx
            state.next_scene_idx = None
            state.current_scene_started = state.current_ticks
            state.entering_scene = True

        # clean screen for this frame
        state.screen.fill("black")
    
    def finish_frame(self, state: GameState):
        # clean up scene management flags
        state.entering_scene = False
        state.exiting_scene = False

        # show screen changes
        pygame.display.flip()

        # limit frame rate by 60 per seconds
        state.clock.tick(60)
    
    def finish_pygame(self):
        pygame.quit()
    
    def run(self):
        self.init_pygame()
        screen = self.init_screen()
        state = GameState(screen)
        game_context = GameContext(state)

        while state.running:
            self.init_frame(state)
            
            current_scene = self.setup.scenes[state.current_scene_idx]

            if state.entering_scene:
                current_scene.load(game_context)
                current_scene.start(game_context)
            
            current_scene.update(game_context)
            current_scene.draw(game_context)

            if state.exiting_scene:
                current_scene.exit(game_context)
            
            self.finish_frame(state)

        self.finish_pygame()
