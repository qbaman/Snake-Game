# Snake game used to show data structures and algorithms.
# Keys: Arrows move, A auto-play, F switch solver, Q queue mode,
#       D debug list, B sort benchmark, P pause, S speed.

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
    # Draw faint lines so the board looks like squares
    for x in range(0, WINDOW_W, CELL):
        pygame.draw.line(surf, GREY, (x, 0), (x, WINDOW_H))
    for y in range(0, WINDOW_H, CELL):
        pygame.draw.line(surf, GREY, (0, y), (WINDOW_W, y))

def draw_cell(surf, pos, color):
    # Draw one square at (column, row)
    x, y = pos
    pygame.draw.rect(surf, color, (x * CELL, y * CELL, CELL, CELL))

def game_over(screen, score, font):
    # Simple “game over” screen. Any key closes it.
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
    # Start Pygame and the game window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Unit 24 Snake")
    clock = pygame.time.Clock()

    # Pick a basic font that always exists
    pygame.font.init()
    font = pygame.font.Font(None, 24)

    # Make a snake in the middle and one piece of food
    snake = Snake((GRID_W // 2, GRID_H // 2))
    food = random_empty(set(snake.body))
    score = 0

    # Feature switches (you can toggle these with keys)
    AUTO = False          # A: the computer plays for you
    QUEUE_MODE = False    # Q: store arrow presses in order
    SHOW_DEBUG = True     # D: show the small step list on the left
    SOLVER = "A*"         # F: A* (smart) or BFS (simple)
    PAUSED = False        # P: stop the game timer
    SPEED = "NORMAL"      # S: NORMAL or FAST

    # Small pieces of memory we use while the game runs
    input_queue = deque()           # remembers your arrow presses
    debug_events = deque(maxlen=8)  # remembers last few steps
    bench_msg = None                # text from sort benchmark
    bench_timeleft = 0.0            # how long to keep that text
    path = None                     # blue path the solver found
    last_solver_stats = None        # numbers about the last path

    # Two helpers that “log” the steps we take each frame
    def trace_push(stk, label):
        stk.push(label); debug_events.append(f"+ {label}")
    def trace_pop(stk):
        if not stk.is_empty(): debug_events.append(f"- {stk.pop()}")

    # Ask a solver (A* or BFS) for a path and timing info
    def compute_path_and_stats(snk, target):
        body = list(snk.body)
        blocked = set(body[1:-1])      # head is free; tail moves next
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
        callstack = Stack()          # shows the order of actions
        trace_push(callstack, "tick")

        # --- 1) READ INPUT (keys, window close) ---
        trace_push(callstack, "input")
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:   # queue mode on/off
                    QUEUE_MODE = not QUEUE_MODE
                elif e.key == pygame.K_a: # auto on/off
                    AUTO = not AUTO; path = None
                elif e.key == pygame.K_d: # debug on/off
                    SHOW_DEBUG = not SHOW_DEBUG
                elif e.key == pygame.K_f: # switch solver
                    SOLVER = "BFS" if SOLVER == "A*" else "A*"; path = None
                elif e.key == pygame.K_p: # pause on/off
                    PAUSED = not PAUSED
                elif e.key == pygame.K_s: # normal/fast
                    SPEED = "FAST" if SPEED == "NORMAL" else "NORMAL"
                elif e.key == pygame.K_b: # run sort demo
                    t_merge = time_sort(mergesort, n=5000, trials=1)
                    t_quick = time_sort(quicksort, n=5000, trials=1)
                    bench_msg = f"Bench 5k: merge {t_merge:.3f}s | quick {t_quick:.3f}s"
                    bench_timeleft = 3.0
                elif e.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    # Map the arrow key to a direction (dx, dy)
                    dirmap = {pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1),
                              pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)}
                    dx, dy = dirmap[e.key]
                    # Queue stores it; manual play sets it now
                    if QUEUE_MODE and not AUTO: input_queue.append((dx, dy))
                    else: snake.set_dir(dx, dy)
        trace_pop(callstack)

        # Use one queued arrow per frame (only when playing manually)
        if not PAUSED and QUEUE_MODE and input_queue and not AUTO:
            dx, dy = input_queue.popleft()
            snake.set_dir(dx, dy)

        # --- 2) PLAN (only in auto mode) ---
        trace_push(callstack, "plan")
        if AUTO and not PAUSED:
            p, stats = compute_path_and_stats(snake, food)
            # Quick safety check so we don’t plan into ourselves
            if p and len(p) > 1:
                nx, ny = p[1]
                body_now = set(list(snake.body)[:-1])
                if not in_bounds(nx, ny) or (nx, ny) in body_now:
                    p, stats = compute_path_and_stats(snake, food)
            # Turn the snake toward the next path step
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

        # --- 3) UPDATE (move snake, check for hits/food) ---
        if not PAUSED:
            trace_push(callstack, "move"); snake.move(); trace_pop(callstack)

            trace_push(callstack, "collide")
            hx, hy = snake.head()
            # Hit a wall or yourself? Then finish the game loop.
            if not in_bounds(hx, hy) or (hx, hy) in list(snake.body)[1:]:
                running = False
            # Ate the food? Add score, grow, drop new food.
            if (hx, hy) == food:
                score += 1
                snake.grow()
                food = random_empty(set(snake.body))
                path = None
            trace_pop(callstack)

        # --- 4) DRAW (make things visible) ---
        trace_push(callstack, "draw")
        screen.fill(BLACK)
        draw_grid(screen)
        for seg in snake.body: draw_cell(screen, seg, GREEN)
        draw_cell(screen, food, RED)
        if AUTO and path:
            for cell in path[1:-1]: draw_cell(screen, cell, BLUE)

        # Top line: status text
        hud = font.render(
            f"Score: {score} | Auto: {'ON' if AUTO else 'OFF'} (A) | Queue: {'ON' if QUEUE_MODE else 'OFF'} (Q) | "
            f"Debug: {'ON' if SHOW_DEBUG else 'OFF'} (D) | Solver: {SOLVER} (F) | "
            f"Paused: {'ON' if PAUSED else 'OFF'} (P) | Speed: {SPEED} (S) | Bench (B)",
            True, WHITE)
        screen.blit(hud, (8, 8))

        # Second line: numbers from the solver
        if last_solver_stats and AUTO:
            s, visited, steps, secs = last_solver_stats
            screen.blit(font.render(f"{s}: visited {visited}, path {steps} steps, {secs:.3f}s", True, WHITE), (8, 28))

        # Queue preview: shows the next arrows that will play
        if QUEUE_MODE and input_queue:
            arrows = {(0,-1):'↑',(0,1):'↓',(-1,0):'←',(1,0):'→'}
            preview = ''.join(arrows[d] for d in list(input_queue)[:12])
            screen.blit(font.render(f"Queue: {len(input_queue)} [{preview}]", True, WHITE), (8, 46))

        # Small list of recent steps (“stack view”)
        if SHOW_DEBUG:
            y = 64
            for ev in list(debug_events):
                screen.blit(font.render(ev, True, WHITE), (8, y)); y += 16

        # Pause note
        if PAUSED:
            screen.blit(font.render("PAUSED — press P to resume", True, WHITE),
                        (20, WINDOW_H // 2 - 12))

        trace_pop(callstack); trace_pop(callstack)

        # Show one-off benchmark message for a few seconds
        if bench_timeleft > 0:
            bench_timeleft -= 1.0 / FPS
            screen.blit(font.render(bench_msg, True, WHITE), (8, WINDOW_H - 26))

        # Put this frame on screen
        pygame.display.flip()

        # Control how fast the game runs
        speed_mult = 2 if SPEED == "FAST" else 1
        clock.tick(FPS * speed_mult)

    # End screen
    game_over(screen, score, font)
    pygame.quit()

if __name__ == "__main__":
    main()