from . import anchors
from pygame import Vector2
from pygame.rect import Rect


class TransformationData:
    def __init__(self,
                 position: Vector2 | tuple[float, float] = (0, 0),
                 scale: Vector2 | tuple[float, float] = (1, 1),
                 rotation: float = 0,
                 anchor: Vector2 | tuple[float, float] = anchors.center):
        self.position = normalize_coordinate_to_vector(position)
        self.scale = normalize_coordinate_to_vector(scale)
        self.rotation = rotation
        self.anchor = normalize_coordinate_to_vector(anchor)
    
    def apply_position_to_rect(self, rect: Rect):
        x = self.position.x - rect.width * self.anchor.x
        y = self.position.y - rect.height * self.anchor.y
        rect.topleft = (x, y)


def create_transformation_zero() -> TransformationData:
    return TransformationData((0, 0), (1, 1), 0)


def normalize_coordinate_to_vector(position):
    if isinstance(position, Vector2):
        return position
    if isinstance(position, tuple):
        return Vector2(position[0], position[1])
