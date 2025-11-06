import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def ask_llm():
    question = input("You (ask): ")
    if not question:
        return
    try:
        response = requests.post(f"{BASE_URL}/ask", json={"question": question})
        data = response.json()
        print("LLM:", data.get("answer") or data.get("error"))
    except Exception as e:
        print("Request failed:", e)

def clean_text():
    text = input("You (raw text to clean): ")
    if not text:
        return
    try:
        response = requests.post(f"{BASE_URL}/clean", json={"text": text})
        data = response.json()
        print("Server response:", json.dumps(data, indent=2))
    except Exception as e:
        print("Request failed:", e)

def extract_info():
    try:
        response = requests.get(f"{BASE_URL}/extract")
        data = response.json()
        print("Extracted info:", json.dumps(data, indent=2))
    except Exception as e:
        print("Request failed:", e)


def classify_feedback():
    try:
        response = requests.get(f"{BASE_URL}/classify_feedback")
        data = response.json()
        
        if "error" in data:
            print("Error:", data["error"])
            return

        # Just show the simple success message from the server
        print(data.get("message", "Feedback classification complete."))
        print("Full results saved in 'feedback_summary.json'.\n")

    except Exception as e:
        print("Request failed:", e)

def summarise_film():
    try:
        response = requests.get(f"{BASE_URL}/summarise_film")
        data = response.json()
        print("Film Summary:", data.get("summary") or data.get("error"))
    except Exception as e:
        print("Request failed:", e)

def summarise_document():
    try:
        response = requests.get(f"{BASE_URL}/summarise")
        data = response.json()
        print("Constrained summary:", data.get("preview"))
    except Exception as e:
        print("Request failed:", e)

def main():
    print("Interactive LLM client!")
    print("Type 'exit' to quit at any time.\n")

    while True:
        choice = input("Choose endpoint (ask / clean / extract / classify / film_summary ): ").strip().lower()
        if choice == "exit":
            break
        elif choice == "ask":
            ask_llm()
        elif choice == "clean":
            clean_text()
        elif choice == "extract":
            extract_info()
        elif choice == "classify":
            classify_feedback()
        elif choice == "film_summary":
            summarise_film()


        else:
            print("Invalid choice. Please choose 'ask', 'clean', 'extract', 'classify' or 'film_summary'.")

    print("Goodbye!")

if __name__ == "__main__":
    main()
