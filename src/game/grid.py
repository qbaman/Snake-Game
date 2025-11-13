import random
from .constants import GRID_W, GRID_H

def in_bounds(x, y):
    return 0 <= x < GRID_W and 0 <= y < GRID_H

def random_empty(occupied):
    # Fast path
    if len(occupied) >= GRID_W * GRID_H:
        raise ValueError("Grid is full; no empty cells available.")
    while True:
        p = (random.randrange(GRID_W), random.randrange(GRID_H))
        if p not in occupied:
            return p
