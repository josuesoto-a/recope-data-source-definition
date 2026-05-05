import json
import csv
from pathlib import Path


def transform_plantel_prices(input_path: Path, output_path: Path):

    with open(input_path, "r") as file:
        data = json.load(file)

    if not data:
        raise ValueError("No data to transform")

    fieldnames = [
        "date",
        "product",
        "price_crc",
        "tax_crc",
        "base_price_crc",
        "unit",
        "product_id",
        "update_date",
        "source",
        "ingestion_timestamp"
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in data:
            writer.writerow(row)

    print(f"Rows written: {len(data)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":

    INPUT_PATH = Path(
        "data/processed/plantel_prices_cleaned.json"
    )

    OUTPUT_PATH = Path(
        "data/processed/plantel_prices.csv"
    )

    transform_plantel_prices(INPUT_PATH, OUTPUT_PATH)