# Tests for BFS and A* on a small grid.

from src.game.pathfinding import bfs, astar

def test_bfs_astar_equal_length_on_open_grid():
    # Simple straight line: both should find the same shortest path length
    start, goal = (0, 0), (5, 0)
    blocked, W, H = set(), 10, 10
    p1 = bfs(start, goal, blocked, W, H)
    p2 = astar(start, goal, blocked, W, H)
    assert p1[0] == start and p1[-1] == goal
    assert p2[0] == start and p2[-1] == goal
    assert len(p1) == len(p2)

def test_no_path_when_blocked_wall():
    # A solid vertical wall between start and goal → no path
    start, goal = (0, 0), (2, 0)
    blocked = {(1, 0), (1, 1), (1, 2), (1, 3)}  # closes every gap on 4x4 grid
    W, H = 4, 4
    assert bfs(start, goal, blocked, W, H) is None
    assert astar(start, goal, blocked, W, H) is None
