import pygame
import pygame.gfxdraw
import time

pygame.init()
screen = pygame.display.set_mode((400, 400))
screen.fill((0, 0, 0))

# Try gfxdraw filled_circle with alpha directly on screen
try:
    pygame.gfxdraw.filled_circle(screen, 200, 200, 100, (255, 0, 0, 128))
    print("gfxdraw.filled_circle SUCCESS")
except Exception as e:
    print(f"gfxdraw.filled_circle FAILED: {e}")

pygame.display.flip()
time.sleep(1)
pygame.quit()
