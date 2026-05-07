import requests
import json
import os
from datetime import datetime

from scripts.utils.logger import get_logger

# Logger del módulo
logger = get_logger("fetch_plantel_prices")

URL = "https://api.recope.go.cr/ventas/precio/plantel"

def fetch_plantel_prices():
    try:
        logger.info("Starting plantel prices fetch")

        response = requests.get(URL, timeout=15)
        response.raise_for_status()

        data = response.json()

        os.makedirs("data/raw", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"data/raw/plantel_prices_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logger.info(f"Plantel data saved to: {file_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error during plantel fetch: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error in fetch_plantel_prices: {e}")
        raise


if __name__ == "__main__":
    fetch_plantel_prices()