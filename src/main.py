import pygame
from .game.constants import *

def draw_grid(surf):
    for x in range(0, WINDOW_W, CELL):
        pygame.draw.line(surf, GREY, (x, 0), (x, WINDOW_H))
    for y in range(0, WINDOW_H, CELL):
        pygame.draw.line(surf, GREY, (0, y), (WINDOW_W, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Unit 24 Snake")
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        draw_grid(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
