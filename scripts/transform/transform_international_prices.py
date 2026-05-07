import json
import csv
from pathlib import Path

from scripts.utils.logger import get_logger

logger = get_logger("transform_international_prices")


def transform_international_prices(input_path: Path, output_path: Path):

    try:
        logger.info(f"Starting transformation | input={input_path}")

        with open(input_path, "r") as file:
            data = json.load(file)

        if not data:
            raise ValueError("No data to transform")

        fieldnames = [
            "date_start",
            "date_end",
            "product",
            "price_usd",
            "product_id",
            "currency",
            "source",
            "ingestion_timestamp"
        ]

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for row in data:
                writer.writerow(row)

        logger.info(
            f"Transformation completed | rows={len(data)} | output={output_path}"
        )

    except Exception as e:
        logger.exception(f"Error in transform_international_prices: {e}")
        raise


if __name__ == "__main__":

    INPUT_PATH = Path("data/processed/international_prices_cleaned.json")
    OUTPUT_PATH = Path("data/processed/international_prices.csv")

    transform_international_prices(INPUT_PATH, OUTPUT_PATH)