import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.game.snake import Snake

def test_move_and_grow():
    s = Snake((3,3))
    # initial length 3
    assert len(s.body) == 3
    s.set_dir(1,0); s.move()
    assert s.head() == (4,3)
    # grow adds a segment after next move
    s.grow()
    s.move()
    assert len(s.body) == 4
