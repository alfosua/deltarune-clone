from engine import *


class PlayerInput:
    def __init__(self, context: GameContext):
        self.context = context
    
    def get_move_axis(self):
        keys_pressed = self.context.get_keys_pressed()
        move_axis = Vector2(0, 0)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_j]:
            move_axis.x -= 1
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_l]:
            move_axis.x += 1
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_i]:
            move_axis.y -= 1
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_k]:
            move_axis.y += 1
        return move_axis
    
    def is_next_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_RIGHT] or keys_down[pygame.K_d] or keys_down[pygame.K_l] or keys_down[pygame.K_UP] or keys_down[pygame.K_w] or keys_down[pygame.K_i]
    
    def is_previous_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_LEFT] or keys_down[pygame.K_a] or keys_down[pygame.K_j] or keys_down[pygame.K_DOWN] or keys_down[pygame.K_s] or keys_down[pygame.K_k]
    
    def is_up_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_UP] or keys_down[pygame.K_w] or keys_down[pygame.K_i]
    
    def is_down_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_DOWN] or keys_down[pygame.K_s] or keys_down[pygame.K_k]
    
    def is_left_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_LEFT] or keys_down[pygame.K_a] or keys_down[pygame.K_j]
    
    def is_right_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_RIGHT] or keys_down[pygame.K_d] or keys_down[pygame.K_l]
    
    def is_confirm_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN] or keys_down[pygame.K_z]
    
    def is_cancel_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_ESCAPE] or keys_down[pygame.K_LSHIFT] or keys_down[pygame.K_RSHIFT] or keys_down[pygame.K_x]
    
    def is_menu_button_down(self):
        keys_down = self.context.get_keys_down()
        return keys_down[pygame.K_TAB] or keys_down[pygame.K_LCTRL] or keys_down[pygame.K_RCTRL] or keys_down[pygame.K_c]
