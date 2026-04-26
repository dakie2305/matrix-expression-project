import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((960, 480), pygame.NOFRAME)
pygame.display.set_caption("Creation 4 - Cud")

# Virtual Grid Constants
VIRTUAL_W = 64
VIRTUAL_H = 32
BLACK = (0, 0, 0)
LED_CYAN = (0, 255, 255)

def get_dynamic_metrics():
    win_w, win_h = screen.get_size()
    pix_w, pix_h = win_w // VIRTUAL_W, win_h // VIRTUAL_H
    p_size = min(pix_w, pix_h)
    off_x = (win_w - (VIRTUAL_W * p_size)) // 2
    off_y = (win_h - (VIRTUAL_H * p_size)) // 2
    return p_size, off_x, off_y

def draw_led(vx, vy, color, p_size, off_x, off_y):
    real_x = off_x + (vx * p_size)
    real_y = off_y + (vy * p_size)
    center = (real_x + p_size // 2, real_y + p_size // 2)
    radius = max(1, p_size // 2 - 1)
    pygame.draw.circle(screen, color, center, radius)

def draw_face(p_size, off_x, off_y, blinking):
    mid_x, mid_y = VIRTUAL_W // 2, VIRTUAL_H // 2
    # Mouth
    w_dots = [(0,0), (0,1), (1,2), (2,1), (3,0), (4,1), (5,2), (6,1), (6,0)]
    mx, my = mid_x - 3, mid_y + 2
    for dx, dy in w_dots:
        draw_led(mx + dx, my + dy, LED_CYAN, p_size, off_x, off_y)
    # Eyes
    eye_y, eye_offset = mid_y - 4, 12
    for side in [-1, 1]:
        ex = mid_x + (side * eye_offset) - 2
        if blinking:
            for i in range(5): draw_led(ex + i, eye_y + 2, LED_CYAN, p_size, off_x, off_y)
        else:
            eye_dots = [(1,0),(2,0),(3,0), (0,1),(1,1),(2,1),(3,1),(4,1), 
                        (0,2),(1,2),(2,2),(3,2),(4,2), (1,3),(2,3),(3,3)]
            for dx, dy in eye_dots:
                draw_led(ex + dx, eye_y + dy, LED_CYAN, p_size, off_x, off_y)

# MAIN LOOP
running = True
blink_timer = 0
is_blinking = False
clock = pygame.time.Clock()
is_seamless = False

while running:
    screen.fill(BLACK)
    p_size, off_x, off_y = get_dynamic_metrics()

    # EVENT HANDLING (The "Input" section)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Escape key
                running = False
            if event.key == pygame.K_q:      # 'Q' key
                running = False
            # Press 'F' to toggle Fullscreen (The ultimate seamless)
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            # Press 'S' to toggle Seamless/Noframe
            if event.key == pygame.K_s:
                is_seamless = not is_seamless
                info = pygame.display.get_wm_info()
                current_w, current_h = screen.get_size()
                if is_seamless:
                    screen = pygame.display.set_mode((current_w, current_h), pygame.NOFRAME)
                else:
                    screen = pygame.display.set_mode((current_w, current_h), pygame.RESIZABLE)
    
    # BLINK LOGIC
    blink_timer += 1
    if not is_blinking and random.randint(1, 100) == 1:
        is_blinking = True
        blink_timer = 0
    if is_blinking and blink_timer > 6:
        is_blinking = False

    # DRAWING
    draw_face(p_size, off_x, off_y, is_blinking)
    
    pygame.display.flip()
    clock.tick(30) # 30FPS

pygame.quit()