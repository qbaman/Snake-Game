import pygame
from .game.constants import *
from .game.snake import Snake

def draw_grid(surf):
    for x in range(0, WINDOW_W, CELL):
        pygame.draw.line(surf, GREY, (x, 0), (x, WINDOW_H))
    for y in range(0, WINDOW_H, CELL):
        pygame.draw.line(surf, GREY, (0, y), (WINDOW_W, y))

def draw_cell(surf, pos, color):
    x, y = pos
    pygame.draw.rect(surf, color, (x*CELL, y*CELL, CELL, CELL))

def in_bounds(x, y):
    return 0 <= x < GRID_W and 0 <= y < GRID_H

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Unit 24 Snake")
    clock = pygame.time.Clock()

    snake = Snake((GRID_W//2, GRID_H//2))
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: snake.set_dir(0, -1)
                elif e.key == pygame.K_DOWN: snake.set_dir(0, 1)
                elif e.key == pygame.K_LEFT: snake.set_dir(-1, 0)
                elif e.key == pygame.K_RIGHT: snake.set_dir(1, 0)

        snake.move()
        hx, hy = snake.head()
        if not in_bounds(hx, hy) or (hx, hy) in list(snake.body)[1:]:
            running = False

        screen.fill(BLACK)
        draw_grid(screen)
        for seg in snake.body:
            draw_cell(screen, seg, (0, 200, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
