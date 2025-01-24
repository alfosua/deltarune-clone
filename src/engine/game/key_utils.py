from .. import pygame


KEYS_TO_TRACK = [
    # Todas las letras
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f,
    pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r,
    pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
    pygame.K_y, pygame.K_z,
    # Todos los números
    pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
    # Teclas direccionales
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
    # Teclas recurrentes
    pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB,
    # Teclas de función
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
    pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,
    # Teclas modificadores
    pygame.K_LSHIFT, pygame.K_LCTRL, pygame.K_LALT, pygame.K_RSHIFT, pygame.K_RCTRL, pygame.K_RALT,
]

def create_key_tracking_dict():
    return { key: False for key in KEYS_TO_TRACK }
