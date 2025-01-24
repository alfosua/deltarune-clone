import random
from engine import *


class Coconut(Scene):
    def load(self, context: GameContext):
        # load image used for the coconut
        self.coconut_image = pygame.image.load("assets/images/coconut.jpg").convert()

    def start(self, context: GameContext) -> None:
        # get from context
        screen = context.get_screen()

        # init state
        self.coconut_pos = Vector2(0, 0)
        self.coconut_dir = Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
        self.limits = Vector2(0, 0)
        self.coconut_speed = 200.0

        # calc random coconut inital position
        self.limits = Vector2(screen.get_width() - self.coconut_image.get_width(), screen.get_height() - self.coconut_image.get_height())
        self.coconut_pos = Vector2(random.randint(0, int(self.limits.x)), random.randint(0, int(self.limits.y)))

    def update(self, context: GameContext) -> None:
        # get grom context
        dt = context.get_delta_time()

        # flip coconut direction if touchings bounds
        if self.coconut_pos.x < 0 or self.coconut_pos.x > self.limits.x:
            self.coconut_dir.x = -self.coconut_dir.x
        if self.coconut_pos.y < 0 or self.coconut_pos.y > self.limits.y:
            self.coconut_dir.y = -self.coconut_dir.y
        
        # update coconut position
        self.coconut_pos = self.coconut_pos + self.coconut_dir * dt * self.coconut_speed

    def draw(self, context: GameContext) -> None:
        # get grom context
        screen = context.get_screen()

        # draw coconut
        screen.blit(self.coconut_image, self.coconut_pos)

    def exit(self, context: GameContext):
        # no logic for exiting
        pass
