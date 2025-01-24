from .state import GameState


class GameContext:
    def __init__(self, state: GameState):
        self.state = state
    
    def get_screen(self):
        return self.state.screen
    
    def quit(self):
        self.state.running = False

    def is_paused(self):
        return self.state.paused

    def get_pause_started_at(self):
        return self.state.pause_started_at

    def set_pause(self, value: bool):
        self.state.paused = value

    def get_screen(self):
        return self.state.screen

    def get_events(self):
        return self.state.events

    def get_screen_rect(self):
        return self.get_screen().get_rect()

    def get_current_ticks(self):
        return self.state.current_ticks

    def get_current_time(self):
        return self.state.current_time

    def get_unscaled_current_ticks(self):
        return self.state.unscaled_current_ticks

    def get_delta_ticks(self):
        return self.state.delta_ticks

    def get_delta_time(self):
        return self.state.delta_time

    def get_keys_pressed(self):
        return self.state.keys_pressed

    def get_keys_down(self):
        return self.state.keys_down

    def get_keys_up(self):
        return self.state.keys_up

    def is_any_key_pressed(self):
        return any(self.state.keys_pressed)

    def is_any_key_down(self):
        return any(value for value in self.state.keys_down.values())

    def is_any_key_up(self):
        return any(value for value in self.state.keys_up.values())
    
    # SCENE MANAGEMENT
    def change_scene(self, new_scene_idx):
        self.state.next_scene_idx = new_scene_idx
        self.state.exiting_scene = True

    def get_scene_idx(self):
        return self.state.current_scene_idx

    def get_current_scene_ticks(self):
        return self.get_current_ticks() - self.state.current_scene_started

    def get_current_scene_time(self):
        return self.get_current_scene_ticks() / 1000

    def get_started_at(self):
        return self.state.current_scene_started

    def is_current(self, scene_idx):
        return self.state.current_scene_idx == scene_idx

    def is_entering_scene(self):
        return self.state.entering_scene

    def is_exiting_scene(self):
        return self.state.exiting_scene
