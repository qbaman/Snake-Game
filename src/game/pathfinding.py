from collections import deque
from heapq import heappush, heappop

def neighbours(p, blocked, W, H):
    x, y = p
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in blocked:
            yield (nx, ny)

def bfs(start, goal, blocked, W, H):
    q = deque([start]); parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal: break
        for nb in neighbours(cur, blocked, W, H):
            if nb not in parent:
                parent[nb] = cur; q.append(nb)
    if goal not in parent: return None
    path=[]; cur=goal
    while cur is not None: path.append(cur); cur=parent[cur]
    return list(reversed(path))

def manhattan(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal, blocked, W, H):
    openh=[]; heappush(openh,(0,start))
    g={start:0}; parent={start:None}
    while openh:
        _, cur = heappop(openh)
        if cur == goal: break
        for nb in neighbours(cur, blocked, W, H):
            t = g[cur] + 1
            if t < g.get(nb, 10**9):
                g[nb] = t; parent[nb] = cur
                heappush(openh, (t + manhattan(nb, goal), nb))
    if goal not in parent: return None
    path=[]; cur=goal
    while cur is not None: path.append(cur); cur=parent[cur]
    return list(reversed(path))
