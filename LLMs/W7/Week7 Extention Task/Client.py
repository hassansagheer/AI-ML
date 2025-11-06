import requests
import os

BASE_URL = "http://127.0.0.1:5000"

def call_summerise_csv():
    path = input("Path to CSV to summarise: ").strip()
    if not os.path.exists(path):
        print("File not found.")
        return
    files = {
        "file": (os.path.basename(path), open(path, "rb"), "text/csv")
    }
    r = requests.post(f"{BASE_URL}/summeriseCSV", files=files)
    try:
        data = r.json()
        print("\n--- LLM Summary ---")
        print(data.get("summary") or data)
    except Exception:
        print(r.text)


def call_anysis():
    path = input("Path to CSV to analyse and generate new CSV: ").strip()
    if not os.path.exists(path):
        print("File not found.")
        return
    files = {
        "file": (os.path.basename(path), open(path, "rb"), "text/csv")
    }
    r = requests.post(f"{BASE_URL}/anysis", files=files)
    if r.status_code == 200:
        outname = "generated_sales_analysis.csv"
        with open(outname, "wb") as f:
            f.write(r.content)
        print(f"Saved generated CSV to: {outname}")
    else:
        print(r.status_code, r.text)


def main():
    while True:
        choice = input("choose: 1) summariseCSV  2) anysis  3) exit : ").strip()
        if choice == "1":
            call_summerise_csv()
        elif choice == "2":
            call_anysis()
        elif choice == "3":
            break
        else:
            print("unknown option")

if __name__ == "__main__":
    main()
