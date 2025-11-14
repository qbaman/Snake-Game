# Unit 24 — Snake (Python)

A small, assessment-focused Snake game that demonstrates **Abstract Data Types (ADTs)** and **algorithms**: Stack (call-stack trace), Queue (input FIFO), Deque (snake body), BFS/A* shortest-path, and mergesort vs quicksort timings. No file/DB storage; everything runs in memory.

## Quick start
```bash
# macOS/Linux
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.main
````

```powershell
# Windows (PowerShell)
py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.main
```

## Controls

* **Arrows**: manual movement
* **A**: Auto on/off (path planner)
* **F**: Toggle **A*** ↔ **BFS** (shows visited/steps/time)
* **Q**: Queue mode on/off (buffers arrows FIFO; one step per tick)
* **D**: Show/hide call-stack debug pane
* **B**: Run mergesort vs quicksort benchmark overlay
* Close window or any key on game-over to exit

## What it demonstrates (for the brief)

* **Deque (Snake body):** O(1) head/tail ops
* **Queue (Input FIFO):** buffered controls executed in order
* **Stack ADT:** on-screen push/pop trace of `input → plan → move → collide → draw`
* **Shortest-path:** **A*** with Manhattan heuristic vs **BFS** (blue path + stats: visited nodes, path length, time)
* **Sorting:** mergesort vs quicksort timings (press **B**)
* **Robustness:** planner replans each tick, treats tail as free, validates next step, allows forced 180° when auto

## Run tests

```bash
# from project root
source .venv/bin/activate   # or Windows activate as above
PYTHONPATH=. pytest -q
```

## Project structure

```
src/
  game/
    adt_stack.py        # Stack ADT (debug pane)
    constants.py        # grid sizes, colors, FPS
    grid.py             # bounds + empty-cell selection
    pathfinding.py      # BFS/A* (+ instrumented stats)
    snake.py            # deque-based snake, grow/move
    sorting_bench.py    # mergesort/quicksort + timing
  main.py               # game loop, HUD, controls
tests/
  test_stack.py
  test_pathfinding.py
  test_snake.py
requirements.txt
```

## Notes

* Python 3.12+ recommended (works on 3.9+). If `pygame` build is problematic on macOS, use `pygame-ce`.
* Designed for Unit 24 evidence: ADTs, algorithm comparison, complexity discussion, tests, and a runnable program.

```
```
