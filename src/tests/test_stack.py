# Tests for our tiny Stack (LIFO). These give evidence that it works.

from src.game.adt_stack import Stack
import pytest

def test_push_pop_and_empty():
    s = Stack()
    # push two items
    s.push(1)
    s.push(2)
    # size should be 2
    assert len(s) == 2
    # pop comes back in reverse order (last in, first out)
    assert s.pop() == 2
    assert s.pop() == 1
    # popping when empty should raise an error
    with pytest.raises(IndexError):
        s.pop()
