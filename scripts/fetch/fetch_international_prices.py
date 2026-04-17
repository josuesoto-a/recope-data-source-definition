import requests
import json
import os
from datetime import datetime

URL = "https://api.recope.go.cr/precio-internacional"

def fetch_data():

    try:

        response = requests.get(URL)

        response.raise_for_status()

        data = response.json()

        os.makedirs("data/raw", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = f"data/raw/international_prices_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4, ensure_ascii=False)

        print("Data saved to:", file_path)

    except Exception as e:

        print("Error:", e)

if __name__ == "__main__":

    fetch_data()