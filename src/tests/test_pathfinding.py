import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.game.pathfinding import bfs, astar

def test_bfs_astar_equal_length_on_open_grid():
    start, goal = (0,0), (5,0)
    blocked, W, H = set(), 10, 10
    p1 = bfs(start, goal, blocked, W, H)
    p2 = astar(start, goal, blocked, W, H)
    assert p1[0] == start and p1[-1] == goal
    assert p2[0] == start and p2[-1] == goal
    assert len(p1) == len(p2)

def test_no_path_when_blocked_wall():
    start, goal = (0,0), (2,0)
    blocked = {(1,0), (1,1), (1,-1), (1,2)}  # vertical wall
    W, H = 4, 4
    assert bfs(start, goal, blocked, W, H) is None
    assert astar(start, goal, blocked, W, H) is None
