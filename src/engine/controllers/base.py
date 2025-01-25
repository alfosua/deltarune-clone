from abc import ABC, abstractmethod
from ..game import GameContext


class ControllerBase(ABC):
    def __init__(self, context: GameContext):
        super().__init__()
        self.__context = context

    @property
    def context(self):
        return self.__context

    @abstractmethod
    def init_update(self):
        pass

    @abstractmethod
    def finish_update(self):
        pass
