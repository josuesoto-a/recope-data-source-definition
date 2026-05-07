import requests
import json
import os
from datetime import datetime

from scripts.utils.logger import get_logger

# LOGGER
logger = get_logger("fetch_consumer_prices")

URL =  "https://api.recope.go.cr/ventas/precio/consumidor"


def fetch_consumer_prices():
    try:
        logger.info("Starting consumer prices fetch")

        response = requests.get(URL, timeout=15)
        response.raise_for_status()

        data = response.json()

        os.makedirs("data/raw", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"data/raw/consumer_prices_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logger.info(f"Consumer data saved to: {file_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error during fetch: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error in fetch_consumer_prices: {e}")
        raise


if __name__ == "__main__":
    fetch_consumer_prices()