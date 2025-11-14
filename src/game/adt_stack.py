# Very small Stack (LIFO). Used for the debug step list.
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
