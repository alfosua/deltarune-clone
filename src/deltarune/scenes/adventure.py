from engine import *

PLAYER_SPEED = 200

STATUS_EXPLORATION = 0
STATUS_BATTLE = 1

TURN_PLAYER = 0
TURN_ENEMY = 1

BATTLE_MENU_MAIN = 0
BATTLE_MENU_FIGHT = 1
BATTLE_MENU_ACT = 2
BATTLE_MENU_MAGIC = 3


class Adventure(Scene):
    def load(self, context: GameContext):
        self.font = pygame.font.SysFont("Arial", 24)

        self.girly_archer_sheet = sprites.load_spritesheet("assets/sprites/charas/linkle-idle.json")
        self.girly_archer = sprites.AnimatedSprite(self.girly_archer_sheet.frames, transform=TransformationData(anchor=anchors.bottomcenter), duration=1/12)
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.girly_archer)

    def start(self, context: GameContext) -> None:
        # status fsm
        self.current_status = STATUS_EXPLORATION
        # exploration
        self.player_pos = Vector2(100, 200)
        # battle
        self.player_team = ["linkle", "linkle", "linkle"]
        self.enemy_team = ["linkle", "linkle", "linkle"]
        self.current_turn = TURN_PLAYER
        # player battle menu
        self.menu_selected_option = 0
        self.menu_selected_chara = 0

        # music
        pygame.mixer.music.load("assets/music/secret.mp3")
        pygame.mixer.music.play(-1)

    def update(self, context: GameContext) -> None:
        dt = context.get_delta_time()
        keys_pressed = context.get_keys_pressed()
        keys_down = context.get_keys_down()

        if self.current_status == STATUS_EXPLORATION:
            if keys_down[pygame.K_SPACE]:
                self.current_status = STATUS_BATTLE

            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                self.player_pos.x -= PLAYER_SPEED * dt
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                self.player_pos.x += PLAYER_SPEED * dt
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                self.player_pos.y -= PLAYER_SPEED * dt
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.player_pos.y += PLAYER_SPEED * dt

        elif self.current_status == STATUS_BATTLE:
            if keys_down[pygame.K_ESCAPE]:
                self.current_status = STATUS_EXPLORATION

        self.girly_archer.set_position(self.player_pos)
        self.sprite_group.update(dt)

    def draw(self, context: GameContext) -> None:
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()

        self.sprite_group.draw(screen)

        if self.current_status == STATUS_BATTLE:
            pygame.draw.rect(screen, "dark blue", (50, screen_rect.bottom - 200 - 50, screen_rect.width - 100, 200))

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()
