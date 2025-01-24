from ..scenes import Scene


class GameSetup:
    def __init__(self,
                 title: str,
                 scenes: list[Scene]):
        self.title = title
        self.scenes = scenes
