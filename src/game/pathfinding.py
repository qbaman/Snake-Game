# Path finding on a square grid.
# We use two algorithms:
#  - BFS: simple, always finds a shortest path (fewest steps) on a grid
#  - A*: faster on average by using a distance guess (the “heuristic”)

from collections import deque
from heapq import heappush, heappop

def neighbours(p, blocked, W, H):
    """Return walkable cells next to p (up, down, left, right)."""
    x, y = p
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        # Inside the grid and not inside the blocked set
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in blocked:
            yield (nx, ny)

def _reconstruct(parent, goal):
    """Build the path by walking back from goal to start using the parent map."""
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def manhattan(a, b):
    """How far two cells are if you can only move in straight lines (no diagonals)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# -------- Basic versions (used by tests) --------

def bfs(start, goal, blocked, W, H):
    """Breadth-First Search: explores layer by layer. Finds a shortest path."""
    q = deque([start])
    parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for nb in neighbours(cur, blocked, W, H):
            if nb not in parent:          # not visited yet
                parent[nb] = cur          # remember how we got here
                q.append(nb)
    if goal not in parent:
        return None
    return _reconstruct(parent, goal)

def astar(start, goal, blocked, W, H):
    """A*: uses a priority queue ordered by (cost so far + distance guess)."""
    openh = []
    heappush(openh, (0, start))           # (priority, cell)
    g = {start: 0}                         # best cost to reach a cell
    parent = {start: None}
    while openh:
        _, cur = heappop(openh)
        if cur == goal:
            break
        for nb in neighbours(cur, blocked, W, H):
            new_cost = g[cur] + 1         # each step costs 1
            if new_cost < g.get(nb, 10**9):
                g[nb] = new_cost
                parent[nb] = cur
                # priority = cost so far + guess to goal
                heappush(openh, (new_cost + manhattan(nb, goal), nb))
    if goal not in parent:
        return None
    return _reconstruct(parent, goal)

# -------- Instrumented versions (return path + a small stat) --------

def bfs_stats(start, goal, blocked, W, H):
    """BFS that also returns how many cells we visited (simple ‘work’ measure)."""
    q = deque([start])
    parent = {start: None}
    visited = 1
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for nb in neighbours(cur, blocked, W, H):
            if nb not in parent:
                parent[nb] = cur
                q.append(nb)
                visited += 1
    if goal not in parent:
        return None, visited
    return _reconstruct(parent, goal), visited

def astar_stats(start, goal, blocked, W, H):
    """A* that also returns how many nodes we pushed/explored."""
    openh = []
    heappush(openh, (0, start))
    g = {start: 0}
    parent = {start: None}
    visited = 1
    while openh:
        _, cur = heappop(openh)
        if cur == goal:
            break
        for nb in neighbours(cur, blocked, W, H):
            new_cost = g[cur] + 1
            if new_cost < g.get(nb, 10**9):
                g[nb] = new_cost
                parent[nb] = cur
                heappush(openh, (new_cost + manhattan(nb, goal), nb))
                visited += 1
    if goal not in parent:
        return None, visited
    return _reconstruct(parent, goal), visited
