from ..state import GameState


class SceneContext:
    def __init__(self, state: GameState):
        self.state = state

    def change(self, new_scene_idx):
        self.state.next_scene_idx = new_scene_idx
        self.state.exiting_scene = True

    def get_idx(self):
        return self.state.current_scene_idx

    def get_current_ticks(self):
        return self.state.current_ticks - self.state.current_scene_started

    def get_current_time(self):
        return self.get_current_ticks() / 1000

    def get_started_at(self):
        return self.state.current_scene_started

    def is_current(self, scene_idx):
        return self.state.current_scene_idx == scene_idx

    def is_entering(self):
        return self.state.entering_scene

    def is_exiting(self):
        return self.state.exiting_scene
