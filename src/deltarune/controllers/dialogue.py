DEFAULT_DIALOGUE_SPEED = 100


class DialogueController:
    def __init__(self):
        self.ticks = 0
        self.started_at = 0
        self.content = ""
        self.duration = 0
        self.finished = False

    def update_ticks(self, ticks: int):
        self.ticks = ticks
        if self.started_at and self.ticks - self.started_at > self.duration:
            self.finished = True

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
    
    def is_finished(self):
        return self.finished