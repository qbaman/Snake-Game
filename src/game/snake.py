from collections import deque

class Snake:
    def __init__(self, head):
        x, y = head
        # start moving right; safe initial body
        self.body = deque([(x, y), (x - 1, y), (x - 2, y)])
        self.dx, self.dy = 1, 0
        self._grow_pending = 0

    def head(self):
        return self.body[0]

    def set_dir(self, dx, dy, force=False):
        # block 180° reversals unless forced (used by auto)
        if not force and (dx, dy) == (-self.dx, -self.dy):
            return
        self.dx, self.dy = dx, dy

    def move(self):
        hx, hy = self.head()
        nx, ny = hx + self.dx, hy + self.dy
        self.body.appendleft((nx, ny))
        if self._grow_pending > 0:
            self._grow_pending -= 1
        else:
            self.body.pop()

    def grow(self):
        self._grow_pending += 1
