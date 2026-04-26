import pygame
import random

# Initialize Pygame with a resizable window
pygame.init()
screen = pygame.display.set_mode((960, 480), pygame.RESIZABLE)
pygame.display.set_caption("Auto-Scaling Creature")

# Virtual Grid Constants (The "Brain" always thinks in 64x32)
VIRTUAL_W = 64
VIRTUAL_H = 32

# Colors
BLACK = (0, 0, 0)
LED_CYAN = (0, 255, 255)

def get_dynamic_metrics():
    """Calculates pixel size and offsets based on current window size."""
    win_w, win_h = screen.get_size()
    # Calculate how big each 'LED' should be to fit the window
    pix_w = win_w // VIRTUAL_W
    pix_h = win_h // VIRTUAL_H
    # Use the smaller one to keep the aspect ratio square
    pixel_size = min(pix_w, pix_h)
    # Calculate offsets to keep the face perfectly centered if window aspect ratio changes
    offset_x = (win_w - (VIRTUAL_W * pixel_size)) // 2
    offset_y = (win_h - (VIRTUAL_H * pixel_size)) // 2
    return pixel_size, offset_x, offset_y

def draw_led(vx, vy, color, p_size, off_x, off_y):
    """Draws a virtual pixel (vx, vy) translated to real screen space."""
    real_x = off_x + (vx * p_size)
    real_y = off_y + (vy * p_size)
    # Drawing the 'bead' look
    center = (real_x + p_size // 2, real_y + p_size // 2)
    radius = max(1, p_size // 2 - 1) # Ensure radius is at least 1
    pygame.draw.circle(screen, color, center, radius)

def draw_face(p_size, off_x, off_y, blinking):
    mid_x = VIRTUAL_W // 2
    mid_y = VIRTUAL_H // 2
    
    # Mouth 'w' relative to center
    # This shape is defined by offsets from a starting point
    w_dots = [(0,0), (0,1), (1,2), (2,1), (3,0), (4,1), (5,2), (6,1), (6,0)]
    mx, my = mid_x - 3, mid_y + 2
    for dx, dy in w_dots:
        draw_led(mx + dx, my + dy, LED_CYAN, p_size, off_x, off_y)
        
    # Eyes relative to center
    eye_y = mid_y - 4
    eye_offset = 12
    
    for side in [-1, 1]: # -1 for Left, 1 for Right
        ex = mid_x + (side * eye_offset) - 2
        if blinking:
            for i in range(5): draw_led(ex + i, eye_y + 2, LED_CYAN, p_size, off_x, off_y)
        else:
            # Diamond shape eye
            eye_dots = [(1,0),(2,0),(3,0), (0,1),(1,1),(2,1),(3,1),(4,1), 
                        (0,2),(1,2),(2,2),(3,2),(4,2), (1,3),(2,3),(3,3)]
            for dx, dy in eye_dots:
                draw_led(ex + dx, eye_y + dy, LED_CYAN, p_size, off_x, off_y)

# Main Loop
running = True
blink_timer = 0
is_blinking = False

while running:
    screen.fill(BLACK)
    p_size, off_x, off_y = get_dynamic_metrics()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    # Blink logic
    blink_timer += 1
    if not is_blinking and random.randint(1, 100) == 1:
        is_blinking = True
        blink_timer = 0
    if is_blinking and blink_timer > 6: is_blinking = False

    draw_face(p_size, off_x, off_y, is_blinking)
    
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()