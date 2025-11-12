import pygame
from .game.constants import *
from .game.snake import Snake
from .game.grid import in_bounds, random_empty
from .game import pathfinding

def draw_grid(surf):
    for x in range(0, WINDOW_W, CELL):
        pygame.draw.line(surf, GREY, (x, 0), (x, WINDOW_H))
    for y in range(0, WINDOW_H, CELL):
        pygame.draw.line(surf, GREY, (0, y), (WINDOW_W, y))

def draw_cell(surf, pos, color):
    x, y = pos
    pygame.draw.rect(surf, color, (x * CELL, y * CELL, CELL, CELL))

def game_over(screen, score, font):
    screen.fill(BLACK)
    msg = font.render(f"Game Over. Score: {score}. Press any key to exit.", True, WHITE)
    screen.blit(msg, (20, WINDOW_H // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
                waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Unit 24 Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    snake = Snake((GRID_W // 2, GRID_H // 2))
    food = random_empty(set(snake.body))
    score = 0

    AUTO = False
    path = None

    def compute_path(snk, target):
        body = list(snk.body)
        blocked = set(body[1:-1])  # head free; tail cell treated as free this tick
        return pathfinding.astar(snk.head(), target, blocked, GRID_W, GRID_H) \
            or pathfinding.bfs(snk.head(), target, blocked, GRID_W, GRID_H)

    running = True
    while running:
        # input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    snake.set_dir(0, -1)
                elif e.key == pygame.K_DOWN:
                    snake.set_dir(0, 1)
                elif e.key == pygame.K_LEFT:
                    snake.set_dir(-1, 0)
                elif e.key == pygame.K_RIGHT:
                    snake.set_dir(1, 0)
                elif e.key == pygame.K_a:
                    AUTO = not AUTO
                    path = None

        # auto-path planning: replan every tick and validate next step
        if AUTO:
            p = compute_path(snake, food)
            if p and len(p) > 1:
                nx, ny = p[1]
                body_now = set(list(snake.body)[:-1])  # tail vacates; exclude it
                if not in_bounds(nx, ny) or (nx, ny) in body_now:
                    p = compute_path(snake, food)
            if p and len(p) > 1:
                nx, ny = p[1]
                dx, dy = nx - snake.head()[0], ny - snake.head()[1]
                snake.set_dir(dx, dy, force=True)  # allow 180° when planner decides
                path = p
            else:
                path = None

        # update
        snake.move()
        hx, hy = snake.head()
        if not in_bounds(hx, hy) or (hx, hy) in list(snake.body)[1:]:
            running = False

        if (hx, hy) == food:
            score += 1
            snake.grow()
            food = random_empty(set(snake.body))
            path = None  # recompute next tick

        # draw
        screen.fill(BLACK)
        draw_grid(screen)
        for seg in snake.body:
            draw_cell(screen, seg, GREEN)
        draw_cell(screen, food, RED)

        if AUTO and path:
            for cell in path[1:-1]:
                draw_cell(screen, cell, BLUE)

        hud = font.render(f"Score: {score} | Auto: {'ON' if AUTO else 'OFF'} (A)", True, WHITE)
        screen.blit(hud, (8, 8))

        pygame.display.flip()
        clock.tick(FPS)

    game_over(screen, score, font)
    pygame.quit()

if __name__ == "__main__":
    main()
