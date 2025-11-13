# maze_visual.py
from typing import List, Tuple
from pyamaze import maze, agent
import time

##setting a tuple for the data
Cell = Tuple[int, int]

###explaing to the llm how to animate (providing small instructions )
def animate(m: maze, path: List[Cell], delay: int = 300,
            footprints: bool = True, color: str = "red", **kwargs):
    """
    Manual animation: move the agent step by step through the path.
    Uses Tk's window update directly (m._win.update()).
    Extra kwargs (like 'step') are ignored for compatibility.
    """
    ##what to do if there is no path
    if not path:
        agent(m, shape='arrow', footprints=footprints, filled=True, color=color)
        m.run()
        return

    r0, c0 = path[0]
    a = agent(m, x=r0, y=c0, shape='arrow', footprints=footprints, filled=True, color=color)

    ##draw on each tick
    for (r, c) in path[1:]:
        a.x, a.y = r, c
        m._win.update()            # refresh Tk window
        time.sleep(delay / 1000.0) # ms -> s
    ##run
    m.run()
