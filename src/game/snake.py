from collections import deque

class Snake:
    def __init__(self, start):
        self.body = deque([start, (start[0]-1, start[1]), (start[0]-2, start[1])])
        self.dir = (1, 0)
        self.grow_pending = 0

    def set_dir(self, dx, dy, force=False):
        if not force and (dx, dy) == (-self.dir[0], -self.dir[1]):
            return
        self.dir = (dx, dy)

    def head(self): return self.body[0]

    def move(self):
        hx, hy = self.head()
        nx, ny = hx + self.dir[0], hy + self.dir[1]
        self.body.appendleft((nx, ny))
        if self.grow_pending: self.grow_pending -= 1
        else: self.body.pop()

    def grow(self, n=1): self.grow_pending += n
