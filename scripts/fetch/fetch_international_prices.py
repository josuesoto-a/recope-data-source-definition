import requests
import json
import os
from datetime import datetime

from scripts.utils.logger import get_logger

# Logger específico del módulo
logger = get_logger("fetch_international_prices")

URL = "https://api.recope.go.cr/precio-internacional"


def fetch_international_prices():
    try:
        logger.info("Starting international prices fetch")

        response = requests.get(URL, timeout=15)
        response.raise_for_status()

        # VALIDACIÓN CRÍTICA
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError(f"Invalid response type: {content_type}")

        data = response.json()

        os.makedirs("data/raw", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"data/raw/international_prices_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logger.info(f"International data saved to: {file_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error during international fetch: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error in fetch_international_prices: {e}")
        raise


if __name__ == "__main__":
    fetch_international_prices()