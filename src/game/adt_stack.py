class Stack:
    def __init__(self): self._d = []
    def push(self, x): self._d.append(x)
    def pop(self):
        if not self._d: raise IndexError("pop from empty stack")
        return self._d.pop()
    def is_empty(self): return len(self._d) == 0
    def __len__(self): return len(self._d)
