import random
from engine import *


class Wip(Scene):
    def load(self, context: GameContext):
        # get from context
        screen_rect = context.get_screen_rect()

        # load font from system
        self.font_main = pygame.font.SysFont("Arial", 24)

        # load image to use
        self.image_wip = pygame.image.load("assets/images/wip.png").convert_alpha()
        self.image_wip = pygame.transform.scale(self.image_wip, (screen_rect.width, screen_rect.width * self.image_wip.get_height() / self.image_wip.get_width()))
        
        # pre-render texts
        self.text_press_spacebar_anytime = self.font_main.render("Press Spacebar Anytime", True, "white")

        # load sounds
        self.sound_kojima = pygame.mixer.Sound("assets/sounds/kojima.mp3")

    def start(self, context: GameContext) -> None:
        # init state
        self.paused_time_elapsed = 0
        self.time_elapsed = 0

        # play secret music
        pygame.mixer.music.load("assets/music/secret.mp3")
        pygame.mixer.music.play(-1)

    def update(self, context: GameContext) -> None:
        # get from context
        keys_down = context.get_keys_down()
        current_time = context.scene.get_current_ticks()
        unescaled_current_ticks = context.get_unscaled_current_ticks()
        pause_started_at = context.get_pause_started_at()
        keys_pressed = context.get_keys_pressed()

        # calc and store timers
        self.time_elapsed = current_time
        self.paused_time_elapsed = (unescaled_current_ticks - pause_started_at) // 1000

        # check input for specific features
        if keys_down[pygame.K_SPACE]:
            self.sound_kojima.play()
        if keys_pressed[pygame.K_ESCAPE]:
            context.set_pause(True)
        else:
            context.set_pause(False)

        # check input for changing scene
        for event in context.get_events():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isnumeric():
                    context.scene.change(int(event.unicode) - 1)

    def draw(self, context: GameContext) -> None:
        # get from context
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()

        # draw wip image
        screen.blit(self.image_wip, (0, screen_rect.centery - self.image_wip.get_height() // 2))
        screen.blit(self.text_press_spacebar_anytime, (screen_rect.centerx - self.text_press_spacebar_anytime.get_width() // 2, screen_rect.bottom - self.text_press_spacebar_anytime.get_height() - 20))
        
        # draw elapsed time counter
        seconds_text = self.font_main.render("You've been in here for {} seconds".format(int(self.time_elapsed)), False, "white")
        screen.blit(seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 50))
        
        # draw paused elapsed time counter
        if context.is_paused():
            paused_seconds_text = self.font_main.render("You've been paused for {} seconds".format(int(self.paused_time_elapsed)), False, "white")
            screen.blit(paused_seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 80))

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()
