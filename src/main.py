import time
import pygame
from collections import deque
from .game.constants import *
from .game.snake import Snake
from .game.grid import in_bounds, random_empty
from .game import pathfinding
from .game.sorting_bench import mergesort, quicksort, time_sort
from .game.adt_stack import Stack

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

    # Feature toggles
    AUTO = False                  # A: auto pathfinding
    QUEUE_MODE = False            # Q: input FIFO queue
    SHOW_DEBUG = True             # D: call-stack pane
    SOLVER = "A*"                 # F: toggle A* / BFS

    # State
    input_queue = deque()
    debug_events = deque(maxlen=8)
    bench_msg = None
    bench_timeleft = 0.0
    path = None
    last_solver_stats = None  # (solver, visited, steps, seconds)

    # Debug helpers using Stack ADT
    def trace_push(stk, label):
        stk.push(label); debug_events.append(f"+ {label}")
    def trace_pop(stk):
        if not stk.is_empty(): debug_events.append(f"- {stk.pop()}")

    def compute_path_and_stats(snk, target):
        body = list(snk.body)
        blocked = set(body[1:-1])  # head free; tail vacates this tick
        t0 = time.perf_counter()
        if SOLVER == "A*":
            p, visited = pathfinding.astar_stats(snk.head(), target, blocked, GRID_W, GRID_H)
        else:
            p, visited = pathfinding.bfs_stats(snk.head(), target, blocked, GRID_W, GRID_H)
        secs = time.perf_counter() - t0
        steps = (len(p) - 1) if p else 0
        return p, (SOLVER, visited, steps, secs)

    running = True
    while running:
        callstack = Stack()
        trace_push(callstack, "tick")

        # --- input ---
        trace_push(callstack, "input")
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    QUEUE_MODE = not QUEUE_MODE
                elif e.key == pygame.K_a:
                    AUTO = not AUTO; path = None
                elif e.key == pygame.K_d:
                    SHOW_DEBUG = not SHOW_DEBUG
                elif e.key == pygame.K_f:
                    SOLVER = "BFS" if SOLVER == "A*" else "A*"
                    path = None
                elif e.key == pygame.K_b:
                    t_merge = time_sort(mergesort, n=5000, trials=1)
                    t_quick = time_sort(quicksort, n=5000, trials=1)
                    bench_msg = f"Bench 5k: merge {t_merge:.3f}s | quick {t_quick:.3f}s"
                    bench_timeleft = 3.0
                elif e.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    dirmap = {pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1), pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)}
                    dx, dy = dirmap[e.key]
                    if QUEUE_MODE and not AUTO: input_queue.append((dx, dy))
                    else: snake.set_dir(dx, dy)
        trace_pop(callstack)

        if QUEUE_MODE and input_queue and not AUTO:
            dx, dy = input_queue.popleft()
            snake.set_dir(dx, dy)

        # --- plan (auto) ---
        trace_push(callstack, "plan")
        if AUTO:
            p, stats = compute_path_and_stats(snake, food)
            if p and len(p) > 1:
                nx, ny = p[1]
                body_now = set(list(snake.body)[:-1])
                if not in_bounds(nx, ny) or (nx, ny) in body_now:
                    p, stats = compute_path_and_stats(snake, food)
            if p and len(p) > 1:
                nx, ny = p[1]
                dx, dy = nx - snake.head()[0], ny - snake.head()[1]
                snake.set_dir(dx, dy, force=True)
                path = p
                last_solver_stats = stats
            else:
                path = None
                last_solver_stats = (SOLVER, 0, 0, 0.0)
        trace_pop(callstack)

        # --- update ---
        trace_push(callstack, "move"); snake.move(); trace_pop(callstack)

        trace_push(callstack, "collide")
        hx, hy = snake.head()
        if not in_bounds(hx, hy) or (hx, hy) in list(snake.body)[1:]:
            running = False
        if (hx, hy) == food:
            score += 1
            snake.grow()
            food = random_empty(set(snake.body))
            path = None
        trace_pop(callstack)

        # --- draw ---
        trace_push(callstack, "draw")
        screen.fill(BLACK)
        draw_grid(screen)
        for seg in snake.body: draw_cell(screen, seg, GREEN)
        draw_cell(screen, food, RED)
        if AUTO and path:
            for cell in path[1:-1]: draw_cell(screen, cell, BLUE)

        hud = font.render(
            f"Score: {score} | Auto: {'ON' if AUTO else 'OFF'} (A) | Queue: {'ON' if QUEUE_MODE else 'OFF'} (Q) | Debug: {'ON' if SHOW_DEBUG else 'OFF'} (D) | Solver: {SOLVER} (F) | Bench (B)",
            True, WHITE)
        screen.blit(hud, (8, 8))

        # second line: solver stats when auto is on
        if last_solver_stats and AUTO:
            s, visited, steps, secs = last_solver_stats
            line2 = font.render(f"{s}: visited {visited}, path {steps} steps, {secs:.3f}s", True, WHITE)
            screen.blit(line2, (8, 28))

        if QUEUE_MODE and input_queue:
            preview = ''.join({(0,-1):'↑',(0,1):'↓',(-1,0):'←',(1,0):'→'}[d] for d in list(input_queue)[:12])
            screen.blit(font.render(f"Queue: {len(input_queue)} [{preview}]", True, WHITE), (8, 46))

        if SHOW_DEBUG:
            y = 64
            for ev in list(debug_events):
                screen.blit(font.render(ev, True, WHITE), (8, y)); y += 16
        trace_pop(callstack); trace_pop(callstack)

        if bench_timeleft > 0:
            bench_timeleft -= 1.0 / FPS
            screen.blit(font.render(bench_msg, True, WHITE), (8, WINDOW_H - 26))

        pygame.display.flip()
        clock.tick(FPS)

    game_over(screen, score, font)
    pygame.quit()

if __name__ == "__main__":
    main()
