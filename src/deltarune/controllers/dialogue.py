from engine import *

DEFAULT_DIALOGUE_SPEED = 100


class DialogueController(ControllerBase):
    def __init__(self, context: GameContext):
        super(DialogueController, self).__init__(context)
        self.ticks = 0
        self.started_at = 0
        self.content = ""
        self.duration = 0
        self.finished = False

    def init_update(self):
        self.ticks = self.context.scene.get_current_ticks()
        if self.started_at and self.ticks - self.started_at > self.duration:
            self.finished = True
    
    def finish_update(self):
        pass

    def start(self, content: str, duration: int = None):
        self.started_at = self.ticks
        self.content = content
        self.duration = duration if duration else len(content) * DEFAULT_DIALOGUE_SPEED
        self.finished = False
    
    def clear(self):
        self.started_at = 0
        self.content = ""
        self.duration = 0
        self.finished = False
    
    def finish(self):
        self.finished = True
    
    @property
    def is_finished(self):
        return self.finished