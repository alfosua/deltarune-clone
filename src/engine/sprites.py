import pygame
from pygame import Surface, Vector2
from pygame.sprite import Sprite

from .resources import load_json_resource
from .transformation import TransformationData, create_transformation_zero


def load_spritesheet(filename: str):
    data_dict = load_json_resource(filename)
    data = SpriteSheetData(**data_dict)
    image = pygame.image.load(data.image_filename).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * data.scale_factor, image.get_height() * data.scale_factor))
    return SpriteSheet(image, data)


class SpriteSheetData:
    def __init__(self, image_filename: str, width: int, height: int, columns = 1, rows = 1, linear_count: int | None = None, offset_x = 0, offset_y = 0, scale_factor = 1):
        self.image_filename = image_filename
        self.width = width
        self.scaled_width = width * scale_factor
        self.height = height
        self.scaled_height = height * scale_factor
        self.columns = columns
        self.rows = rows
        self.linear_count = linear_count
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale_factor = scale_factor


class SpriteSheet:
    def __init__(self, source: Surface, data: SpriteSheetData):
        self.source = source
        self.data = data
        self.frames = self.split()
    
    def split(self) -> list[Surface]:
        result = []
        for i in range(self.data.rows):
            for j in range(self.data.columns):
                location = (self.data.offset_x + self.data.scaled_width * j, self.data.offset_y + self.data.scaled_height * i)
                result.append(self.source.subsurface(pygame.Rect(location, (self.data.scaled_width, self.data.scaled_height))))
                if self.data.linear_count and len(result) == self.data.linear_count:
                    break
        return result


class AnimatedSprite(Sprite):
    def __init__(self, frames: list[Surface], transform: TransformationData = create_transformation_zero(), duration = 1/10):
        super().__init__()
        self.transform = transform
        self.frames = frames
        self.frame_count = len(frames)
        self.current_frame = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.transform.apply_position_to_rect(self.rect)
        
        self.frame_duration = duration
        self.frame_timer = 0

    def set_position(self, position: Vector2 | tuple[float, float]):
        self.transform.position = position
        self.transform.apply_position_to_rect(self.rect)

    def update(self, dt: float):
        self.frame_timer = self.frame_timer + dt

        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.image = self.frames[self.current_frame]
