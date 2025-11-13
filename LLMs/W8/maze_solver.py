# maze_solver.py
from typing import Dict, List, Tuple
from collections import deque
import heapq
from pyamaze import maze

###setting up a tuple for the maze
Cell = Tuple[int, int]  # (row, col)

##defining neighbors for the trees
def _neighbors(m: maze, cell: Cell):
    r, c = cell
    d = m.maze_map[cell]  # {'N':0/1,'E':0/1,'S':0/1,'W':0/1}
    if d.get('N'): yield (r-1, c)
    if d.get('S'): yield (r+1, c)
    if d.get('E'): yield (r, c+1)
    if d.get('W'): yield (r, c-1)

##reconstructing the data
def _reconstruct(came_from: Dict[Cell, Cell], start: Cell, goal: Cell) -> List[Cell]:
    if goal not in came_from and goal != start:
        return []
    cur = goal
    path = [cur]
    while cur != start:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path

##implementation of BFS
def bfs(m: maze, start: Cell, goal: Cell):
    q = deque([start]); visited = {start}; came_from: Dict[Cell, Cell] = {}; expanded = 0
    while q:
        cur = q.popleft(); expanded += 1
        if cur == goal: break
        for nb in _neighbors(m, cur):
            if nb not in visited:
                visited.add(nb); came_from[nb] = cur; q.append(nb)
    return _reconstruct(came_from, start, goal), expanded

###implementation of DFS
def dfs(m: maze, start: Cell, goal: Cell):
    stack = [start]; visited = {start}; came_from: Dict[Cell, Cell] = {}; expanded = 0
    while stack:
        cur = stack.pop(); expanded += 1
        if cur == goal: break
        for nb in _neighbors(m, cur):
            if nb not in visited:
                visited.add(nb); came_from[nb] = cur; stack.append(nb)
    return _reconstruct(came_from, start, goal), expanded

##implementation of A*
def astar(m: maze, start: Cell, goal: Cell):
    def h(a: Cell, b: Cell): return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan
    openh = [(0, start)]; g = {start: 0}; came_from: Dict[Cell, Cell] = {}; expanded = 0
    while openh:
        _, cur = heapq.heappop(openh); expanded += 1
        if cur == goal: break
        for nb in _neighbors(m, cur):
            tentative = g[cur] + 1
            if tentative < g.get(nb, 10**9):
                g[nb] = tentative; came_from[nb] = cur
                f = tentative + h(nb, goal)
                heapq.heappush(openh, (f, nb))
    return _reconstruct(came_from, start, goal), expanded

##running each algotithem
def solve(rows: int, cols: int, algo: str, start: Cell, goal: Cell):
    m = maze(rows, cols)
    m.CreateMaze()  # generate a perfect maze
    algo = (algo or "astar").lower()
    if   algo in ("astar", "a*", "a-star"): path, exp = astar(m, start, goal)
    elif algo == "bfs":                     path, exp = bfs(m, start, goal)
    elif algo == "dfs":                     path, exp = dfs(m, start, goal)
    else:                                   path, exp = astar(m, start, goal)
    return m, path, exp
