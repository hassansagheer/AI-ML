import requests

# URL of your Flask server
URL = "http://127.0.0.1:5000/ask"

print("Talk to the LLM! Type 'exit' to quit.")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    try:
        # Send the question as JSON
        response = requests.post(URL, json={"question": question})
        data = response.json()
        if "answer" in data:
            print("LLM:", data["answer"])
        else:
            print("Error:", data.get("error", "Unknown error"))
    except Exception as e:
        print("Request failed:", e)
