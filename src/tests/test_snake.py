# Basic movement/growth checks for the Snake.

from src.game.snake import Snake

def test_move_and_grow():
    s = Snake((3, 3))
    # Start length is 3
    assert len(s.body) == 3

    # Move one step to the right
    s.set_dir(1, 0)
    s.move()
    assert s.head() == (4, 3)

    # Ask to grow by 1, then move: length should increase
    s.grow()
    s.move()
    assert len(s.body) == 4
