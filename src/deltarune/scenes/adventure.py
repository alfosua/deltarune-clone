from engine import *
from ..inputs import PlayerInput
from ..characters import Character, CharacterAction

PLAYER_SPEED = 200
PLAYER_MINIGAME_SPEED = 0.75
DIALOGUE_SPEED = 100

STATUS_EXPLORATION = 0
STATUS_BATTLE = 1

PLAYER_TURN_STATUS_STRATEGY = 0
PLAYER_TURN_STATUS_ACTION = 1

PLAYER_TURN_ACTION_STATUS_STARTING = 0
PLAYER_TURN_ACTION_STATUS_PREFACE = 1
PLAYER_TURN_ACTION_STATUS_ANIMATION = 2
PLAYER_TURN_ACTION_STATUS_CONCLUSION = 3

ENEMY_TURN_STATUS_STARTING = 0
ENEMY_TURN_STATUS_PREFACE = 1
ENEMY_TURN_STATUS_MINIGAME = 2
ENEMY_TURN_STATUS_CONCLUSION = 3

TURN_PLAYER = 0
TURN_ENEMY = 1


class Adventure(Scene):
    def load(self, context: GameContext):
        screen_rect = context.get_screen_rect()

        self.font = Font("assets/fonts/joystix/joystix monospace.otf", 20)
        self.name_font = Font("assets/fonts/retro_gaming/Retro Gaming.ttf", 30)
        self.dialogue_font = Font("assets/fonts/retro_gaming/Retro Gaming.ttf", 30)

        self.linkle_portrait = pygame.image.load("assets/images/linkle-portrait.jpg").convert_alpha()
        self.linkle_portrait = pygame.transform.scale(self.linkle_portrait, (32 * screen_rect.width // 640, 24 * screen_rect.height // 480))

        self.girly_archer_sheet = sprites.load_spritesheet("assets/sprites/charas/linkle-idle.json")
        self.girly_archer = sprites.AnimatedSprite(self.girly_archer_sheet.frames, transform=TransformationData(anchor=anchors.bottomcenter), duration=1/12)
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.girly_archer)

    def start(self, context: GameContext) -> None:
        self.linkle_chara = Character(
            name="Linkle",
            max_hp=100,
            current_hp=100,
            primary_color="green",
            actions=[
                CharacterAction(
                    name="Fight",
                ),
                CharacterAction(
                    name="Command",
                ),
                CharacterAction(
                    name="Defend",
                ),
                CharacterAction(
                    name="Items",
                ),
                CharacterAction(
                    name="Spare",
                ),
            ],
        )

        # status fsm
        self.current_status = STATUS_EXPLORATION
        # exploration
        self.player_pos = Vector2(100, 200)
        # battle
        self.player_team = [self.linkle_chara, self.linkle_chara, self.linkle_chara]
        self.enemy_team = ["linkle", "linkle", "linkle"]
        self.current_turn = TURN_PLAYER
        # player battle menu
        self.menu_option_cursor = 0
        self.menu_chara_cursor = 0
        # player turn action
        self.player_turn_status = PLAYER_TURN_STATUS_STRATEGY
        self.player_turn_action_queue = list[BattleAction]()
        self.player_turn_action = None
        self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_STARTING
        self.player_turn_action_animation_started_at = None
        # enemy turn action
        self.enemy_turn_status = ENEMY_TURN_STATUS_STARTING
        self.enemy_turn_minigame_started_at = 0
        # enemy minigame
        self.player_hitbox_pos = Vector2(0.5, 0.5)
        # dialogue flow
        self.dialogue_started_at = None
        self.dialogue_content = ""
        self.dialogue_duration = 0
        self.dialogue_finished = False

        # input
        self.input = PlayerInput(context)

        # music
        pygame.mixer.music.load("assets/music/secret.mp3")
        pygame.mixer.music.play(-1)

    def update(self, context: GameContext) -> None:
        current_ticks = context.get_current_scene_ticks()
        dt = context.get_delta_time()

        if self.current_status == STATUS_EXPLORATION:
            if self.input.is_confirm_button_down():
                self.current_status = STATUS_BATTLE

            move_axis = self.input.get_move_axis()

            if move_axis.length_squared() > 0:
                self.player_pos = self.player_pos + move_axis.normalize() * PLAYER_SPEED * dt

        elif self.current_status == STATUS_BATTLE:
            if self.current_turn == TURN_PLAYER:
                if self.player_turn_status == PLAYER_TURN_STATUS_STRATEGY:
                    if self.input.is_cancel_button_down() and self.menu_chara_cursor == 0:
                        self.current_status = STATUS_EXPLORATION

                    if self.input.is_confirm_button_down():
                        if self.menu_chara_cursor == len(self.player_team) - 1:
                            self.player_turn_status = PLAYER_TURN_STATUS_ACTION
                            self.player_turn_action = None
                            self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_STARTING
                            self.player_turn_action_animation_started_at = None
                        caller = self.player_team[self.menu_chara_cursor]
                        action = caller.actions[self.menu_option_cursor]
                        self.player_turn_action_queue.append(BattleAction(caller, action))
                        self.menu_chara_cursor = min(self.menu_chara_cursor + 1, len(self.player_team) - 1)
                        self.menu_option_cursor = 0
                        
                    elif self.input.is_next_button_down():
                        self.menu_option_cursor = (self.menu_option_cursor + 1) % len(self.player_team[self.menu_chara_cursor].actions)

                    elif self.input.is_previous_button_down():
                        self.menu_option_cursor = (self.menu_option_cursor - 1) % len(self.player_team[self.menu_chara_cursor].actions)

                    elif self.input.is_cancel_button_down():
                        self.player_turn_action_queue.pop()
                        self.menu_chara_cursor = max(0, (self.menu_chara_cursor - 1))
                        self.menu_option_cursor = 0

                elif self.player_turn_status == PLAYER_TURN_STATUS_ACTION:
                    if self.player_turn_action_status == PLAYER_TURN_ACTION_STATUS_STARTING:
                        self.player_turn_action = self.player_turn_action_queue.pop(0)
                        self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_PREFACE
                        self.dialogue_started_at = current_ticks
                        self.dialogue_content = f"{self.player_turn_action.caller.name} will {self.player_turn_action.action.name}."
                        self.dialogue_duration = DIALOGUE_SPEED * len(self.dialogue_content)
                        self.dialogue_finished = False

                    elif self.player_turn_action_status == PLAYER_TURN_ACTION_STATUS_PREFACE:
                        if self.dialogue_finished and self.input.is_confirm_button_down():
                            self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_ANIMATION
                            self.player_turn_action_animation_started_at = current_ticks
                            self.dialogue_started_at = None
                            self.dialogue_content = ""
                            self.dialogue_duration = 0
                            self.dialogue_finished = False
                        elif self.dialogue_started_at and current_ticks - self.dialogue_started_at > self.dialogue_duration or self.input.is_confirm_button_down():
                            self.dialogue_finished = True
                    
                    elif self.player_turn_action_status == PLAYER_TURN_ACTION_STATUS_ANIMATION:
                        if current_ticks - self.player_turn_action_animation_started_at > 2000:
                            self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_CONCLUSION
                            self.player_turn_action_animation_started_at = None
                            self.dialogue_started_at = current_ticks
                            self.dialogue_content = f"{self.player_turn_action.caller.name} did {self.player_turn_action.action.name}."
                            self.dialogue_duration = DIALOGUE_SPEED * len(self.dialogue_content)
                            self.dialogue_finished = False

                    elif self.player_turn_action_status == PLAYER_TURN_ACTION_STATUS_CONCLUSION:
                        if self.dialogue_finished and self.input.is_confirm_button_down():
                            self.dialogue_started_at = None
                            self.dialogue_content = ""
                            self.dialogue_duration = 0
                            self.dialogue_finished = False
                            if len(self.player_turn_action_queue) == 0:
                                self.current_turn = TURN_ENEMY
                                self.enemy_turn_status = ENEMY_TURN_STATUS_STARTING
                            else:
                                self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_STARTING
                        elif self.dialogue_started_at and current_ticks - self.dialogue_started_at > self.dialogue_duration or self.input.is_confirm_button_down():
                            self.dialogue_finished = True
            
            elif self.current_turn == TURN_ENEMY:
                    if self.enemy_turn_status == ENEMY_TURN_STATUS_STARTING:
                        self.enemy_turn_status = ENEMY_TURN_STATUS_PREFACE
                        self.dialogue_started_at = current_ticks
                        self.dialogue_content = f"Minion will attack! Prepare to dodge it all."
                        self.dialogue_duration = DIALOGUE_SPEED * len(self.dialogue_content)
                        self.dialogue_finished = False

                    elif self.enemy_turn_status == ENEMY_TURN_STATUS_PREFACE:
                        if self.dialogue_finished and self.input.is_confirm_button_down():
                            self.enemy_turn_status = ENEMY_TURN_STATUS_MINIGAME
                            self.enemy_turn_minigame_started_at = current_ticks
                            self.player_hitbox_pos = Vector2(0.5, 0.5)
                            self.dialogue_started_at = None
                            self.dialogue_content = ""
                            self.dialogue_duration = 0
                            self.dialogue_finished = False
                        elif self.dialogue_started_at and current_ticks - self.dialogue_started_at > self.dialogue_duration or self.input.is_confirm_button_down():
                            self.dialogue_finished = True
                    
                    elif self.enemy_turn_status == ENEMY_TURN_STATUS_MINIGAME:
                        move_axis = self.input.get_move_axis()
                        
                        if move_axis.length_squared() > 0:
                            self.player_hitbox_pos = self.player_hitbox_pos + move_axis.normalize() * PLAYER_MINIGAME_SPEED * dt
                            self.player_hitbox_pos.x = min(max(.08, self.player_hitbox_pos.x), .92)
                            self.player_hitbox_pos.y = min(max(.08, self.player_hitbox_pos.y), .92)

                        if current_ticks - self.enemy_turn_minigame_started_at > 10000:
                            self.enemy_turn_status = ENEMY_TURN_STATUS_CONCLUSION
                            self.enemy_turn_minigame_started_at = 0
                            self.dialogue_started_at = current_ticks
                            self.dialogue_content = f"Minion did attack."
                            self.dialogue_duration = DIALOGUE_SPEED * len(self.dialogue_content)
                            self.dialogue_finished = False

                    elif self.enemy_turn_status == ENEMY_TURN_STATUS_CONCLUSION:
                        if self.dialogue_finished and self.input.is_confirm_button_down():
                            self.dialogue_started_at = None
                            self.dialogue_content = ""
                            self.dialogue_duration = 0
                            self.dialogue_finished = False
                            if len(self.player_turn_action_queue) == 0:
                                self.current_turn = TURN_PLAYER
                                self.player_turn_status = PLAYER_TURN_STATUS_STRATEGY
                                self.menu_chara_cursor = 0
                                self.menu_option_cursor = 0
                            else:
                                self.player_turn_action_status = PLAYER_TURN_ACTION_STATUS_STARTING
                        elif self.dialogue_started_at and current_ticks - self.dialogue_started_at > self.dialogue_duration or self.input.is_confirm_button_down():
                            self.dialogue_finished = True
                

        self.girly_archer.set_position(self.player_pos)
        self.sprite_group.update(dt)

    def draw(self, context: GameContext) -> None:
        screen = context.get_screen()
        current_ticks = context.get_current_scene_ticks()
        screen_rect = context.get_screen_rect()
        screen_ratio = screen_rect.width // 640

        self.sprite_group.draw(screen)

        if self.current_status == STATUS_BATTLE:
            surface_border_color = "#332033"
            dialogue_box_height = 115 * screen_ratio
            dialogue_box_top = screen_rect.bottom - dialogue_box_height
            dialogue_box_left = screen_rect.left
            pygame.draw.line(screen, surface_border_color, (screen_rect.left, dialogue_box_top), (screen_rect.right, dialogue_box_top), 2 * screen_ratio)
            if self.dialogue_started_at:
                dialogue_ticks = current_ticks - self.dialogue_started_at
                dialogue_target = min(dialogue_ticks * len(self.dialogue_content) // self.dialogue_duration, len(self.dialogue_content))
                dialogue_slice = self.dialogue_content if self.dialogue_finished else self.dialogue_content[:dialogue_target]
                dialogue_text = self.dialogue_font.render(dialogue_slice, False, "white")
                screen.blit(dialogue_text, (dialogue_box_left + 32 * screen_ratio, dialogue_box_top + 16 * screen_ratio))

            for i, chara in enumerate(self.player_team):
                is_chara_active = i == self.menu_chara_cursor and self.player_turn_status == PLAYER_TURN_STATUS_STRATEGY
                chara_menu_color = chara.primary_color if is_chara_active else surface_border_color

                chara_menu_width = screen_rect.width // 3
                chara_menu_height = 70 * screen_ratio if is_chara_active else 40 * screen_ratio
                chara_menu_top = screen_rect.bottom - chara_menu_height - dialogue_box_height
                chara_menu_bottom = chara_menu_top + chara_menu_height
                chara_menu_padding_top = 7 * screen_ratio
                chara_menu_padding_right = 9 * screen_ratio
                chara_menu_left = i * chara_menu_width
                chara_menu_right = chara_menu_left + chara_menu_width
                chara_menu_border = 2 * screen_ratio
                chara_menu_lines_left = chara_menu_left + chara_menu_border / 3
                chara_menu_lines_top = chara_menu_top + chara_menu_border / 3
                chara_menu_lines_right = chara_menu_right - chara_menu_border * 2 / 3
                pygame.draw.lines(screen, chara_menu_color, False, [(chara_menu_lines_left, chara_menu_bottom), (chara_menu_lines_left, chara_menu_lines_top), (chara_menu_lines_right, chara_menu_lines_top), (chara_menu_lines_right, chara_menu_bottom)], 2 * screen_ratio)
                chara_hp_text_height = 10 * screen_ratio
                chara_hp_text = self.font.render(f"{chara.current_hp} / {chara.max_hp}", False, "white")
                chara_hp_text = pygame.transform.scale(chara_hp_text, (chara_hp_text_height * chara_hp_text.get_width() / chara_hp_text.get_height(), chara_hp_text_height))
                screen.blit(chara_hp_text, (chara_menu_right - chara_hp_text.get_width() - chara_menu_padding_right, chara_menu_top + chara_menu_padding_top))

                chara_menu_healthbar_width = 76 * screen_ratio
                chara_menu_healthbar_height = 9 * screen_ratio
                chara_menu_healthbar_margin_top = 3 * screen_ratio
                chara_menu_healthbar_margin_left = 4 * screen_ratio
                chara_menu_healthbar_left = chara_menu_right - chara_menu_healthbar_width - chara_menu_padding_right
                chara_menu_healthbar_top = chara_menu_top + chara_menu_padding_top + chara_hp_text.get_height() + chara_menu_healthbar_margin_top
                pygame.draw.rect(screen, chara.primary_color, (chara_menu_healthbar_left, chara_menu_healthbar_top, chara_menu_healthbar_width, chara_menu_healthbar_height))
                chara_hp_label_text_height = 9 * screen_ratio
                chara_hp_label_text = self.font.render(f"HP", False, "white")
                chara_hp_label_text = pygame.transform.scale(chara_hp_label_text, (chara_hp_label_text_height * chara_hp_label_text.get_width() / chara_hp_label_text.get_height(), chara_hp_label_text_height))
                screen.blit(chara_hp_label_text, (chara_menu_healthbar_left - chara_menu_healthbar_margin_left - chara_hp_label_text.get_width(), chara_menu_healthbar_top))

                chara_name_text_height = 15 * screen_ratio
                chara_name_text = self.name_font.render(chara.name, False, "white")
                chara_name_text = pygame.transform.scale(chara_name_text, (chara_name_text_height * chara_name_text.get_width() / chara_name_text.get_height(), chara_name_text_height))
                screen.blit(chara_name_text, (chara_menu_left + 51 * screen_ratio, chara_menu_top + 13 * screen_ratio))

                screen.blit(self.linkle_portrait, (chara_menu_left + 13 * screen_ratio, chara_menu_top + 10 * screen_ratio))

                if is_chara_active:
                    for i, action in enumerate(chara.actions):
                        is_action_active = i == self.menu_option_cursor

                        action_base_color = "orange"
                        action_active_color = "yellow"
                        action_box_margin_bottom = 6 * screen_ratio
                        action_box_height = 26 * screen_ratio
                        action_box_width = 32 * screen_ratio
                        action_box_gap = 4 * screen_ratio
                        action_items_width = len(chara.actions) * action_box_width + (len(chara.actions) - 1) * action_box_gap
                        action_box_left = chara_menu_left + chara_menu_width / 2 - action_items_width / 2 + (action_box_width + action_box_gap) * i
                        action_box_top = chara_menu_bottom - action_box_height - action_box_margin_bottom
                        action_box_bottom = action_box_top + action_box_height
                        action_color = action_active_color if is_action_active else action_base_color
                        pygame.draw.rect(screen, action_color, (action_box_left, action_box_top, action_box_width, action_box_height), 2 * screen_ratio, 1 * screen_ratio)

                        if is_action_active:
                            action_label_text_height = 7 * screen_ratio
                            action_label_text = self.font.render(action.name, False, action_color)
                            action_label_text = pygame.transform.scale(action_label_text, (action_label_text_height * action_label_text.get_width() / action_label_text.get_height(), action_label_text_height))
                            screen.blit(action_label_text, (action_box_left + action_box_width / 2 - action_label_text.get_width() / 2, action_box_bottom))
            
            if self.current_turn == TURN_ENEMY and self.enemy_turn_status == ENEMY_TURN_STATUS_MINIGAME:
                minigame_box_width = 150 * screen_ratio
                minigame_box_height = 150 * screen_ratio
                minigame_box_left = screen_rect.centerx - minigame_box_width // 2
                minigame_box_top = screen_rect.top + 96 * screen_ratio
                pygame.draw.rect(screen, "black", (minigame_box_left, minigame_box_top, minigame_box_width, minigame_box_height))
                pygame.draw.rect(screen, "white", (minigame_box_left, minigame_box_top, minigame_box_width, minigame_box_height), 4 * screen_ratio)

                pygame.draw.circle(screen, "red", (minigame_box_left + self.player_hitbox_pos.x * minigame_box_width, minigame_box_top + self.player_hitbox_pos.y * minigame_box_height), 8 * screen_ratio)

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()


class BattleAction:
    def __init__(self,  caller: Character, action: CharacterAction):
        self.caller = caller
        self.action = action
