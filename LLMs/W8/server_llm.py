# server_llm.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, re, json

# Gemeni parsing 
USE_LLM = False
gemini_model = None

#set up the LLM API
def init_llm():
    
    #setting the API key and model
    global USE_LLM, gemini_model
    load_dotenv()
    USE_LLM = os.getenv("USE_LLM", "0") == "1"
    api_key = os.getenv("GOOGLE_API_KEY", "")
    
    #Try catch to ensure the LLM is set up correctly
    if USE_LLM and api_key:
        try:
            
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            gemini_model = genai.GenerativeModel("gemini-2.5-flash")   ### set the LLM model here!!!###
            print("[LLM] Gemini enabled.")
            
        except Exception as e:
            
            print(f"[LLM] Failed to init Gemini: {e}. Falling back to regex.")
            USE_LLM = False
            
    else:
        
        print("[LLM] Using regex parser.")

## Parsing the request 
def parse_with_regex(text: str):
    
    ####splitting all the data recived by the LLM (Parching it)
    size = re.search(r"(\d+)\s*(?:x|by)\s*(\d+)", text, re.I)
    rows = int(size.group(1)) if size else 10
    cols = int(size.group(2)) if size else 10
    malgo = re.search(r"\b(a\*|a-star|astar|bfs|dfs)\b", text, re.I)
    
    if malgo:
        
        a = malgo.group(1).lower()
        algo = "astar" if a in ("a*", "a-star", "astar") else a
        
    else:
        
        algo = "astar"

    coords = re.findall(r"\((\d+)\s*,\s*(\d+)\)", text)
    start = (int(coords[0][0]), int(coords[0][1])) if len(coords) >= 1 else (1, 1)
    goal  = (int(coords[1][0]), int(coords[1][1])) if len(coords) >= 2 else (rows, cols)

    ## Returns the results parsed for eaiser handleing
    return {"rows": rows, "cols": cols, "algo": algo,
            "start": [start[0], start[1]],
            "goal":  [goal[0], goal[1]]}

## Instructions for the LLM, EXTREAMLY IMPORTENT that this tells the LLM what to do exactly how you want to do it
LLM_SYS = """You convert a user's request about mazes/search into STRICT JSON with keys:
{"rows": int, "cols": int, "algo": "astar|bfs|dfs", "start": [r,c], "goal": [r,c]}
Rules:
- Indexing is 1-based (top-left is [1,1]).
- If size missing, use rows=10, cols=10.
- If algo missing, use "astar".
- If start missing, [1,1]; if goal missing, [rows,cols].
- Output ONLY the JSON object with those keys. No prose, no markdown.
"""

### parseing again but this time we have more valadation checks
def parse_with_llm(text: str):
    
    global gemini_model
    
    try:
        
        prompt = f"{LLM_SYS}\nUser: {text}"
        resp = gemini_model.generate_content(prompt)
        s = (resp.text or "").strip()
        
        # Extract first {...} JSON
        m = re.search(r"\{.*\}", s, re.S)
        
        if not m:
            
            raise ValueError("No JSON found")
        
        obj = json.loads(m.group(0))
        
        # sanity / defaults
        rows = int(obj.get("rows", 10))
        cols = int(obj.get("cols", 10))
        algo = str(obj.get("algo", "astar")).lower()
        algo = "astar" if algo in ("a*", "a-star", "astar") else ("bfs" if algo=="bfs" else ("dfs" if algo=="dfs" else "astar"))
        start = obj.get("start", [1,1]); goal = obj.get("goal", [rows,cols])
        
        return {"rows": rows, "cols": cols, "algo": algo,
                "start": [int(start[0]), int(start[1])],
                "goal":  [int(goal[0]),  int(goal[1])] }
    
    ## parsing failed and will revert back to the defult parsing!!!
    except Exception as e:
        print(f"[LLM] Parse error: {e}; falling back to regex.") 
        return parse_with_regex(text)


##run the app
app = Flask(__name__)
init_llm()

##parse is the route we use for this command
@app.route("/parse", methods=["POST"])
def parse_endpoint():
    
    ###sends data as jason
    data = request.get_json(force=True, silent=True) or {}
    ##gets the request
    q = str(data.get("question", "")).strip()
    
    ##no data/question
    if not q:
        return jsonify({"error": "Provide 'question'"}), 400
    
    ##set the params for the request
    params = parse_with_llm(q) if USE_LLM else parse_with_regex(q)
    return jsonify({"ok": True, "params": params})

###run 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
