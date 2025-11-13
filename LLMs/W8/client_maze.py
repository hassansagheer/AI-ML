import requests
from maze_solver import solve
from maze_visual import animate

##define what URL the server will run on
SERVER = "http://127.0.0.1:5000/parse"

###user guide on what to type
HELP = """
Type a request, e.g.:
  make me a 10 by 10 maze and run A* from (1,1) to (10,10)
  20x20 bfs
  15 by 12 dfs
(type 'exit' to quit)
"""
## inital question logic
def ask_server(question: str):
    r = requests.post(SERVER, json={"question": question}, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(data)
    return data["params"]

##running the client 
def main():
    print(HELP)
    while True:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break
        try:
            p = ask_server(q)
            rows, cols = int(p["rows"]), int(p["cols"])
            algo = p["algo"]
            start = (int(p["start"][0]), int(p["start"][1]))
            goal  = (int(p["goal"][0]), int(p["goal"][1]))
            print(f"[info] Generating {rows}x{cols} maze, solving with {algo.upper()} from {start} to {goal}...")
            m, path, expanded = solve(rows, cols, algo, start, goal)
            print(f"[info] Path length: {len(path)} | Nodes expanded: {expanded}")
            # Manual animation (works on all pyamaze builds)
            animate(m, path, delay=300, footprints=True, color="red")
        except Exception as e:
            print("[error]", e)

if __name__ == "__main__":
    main()
