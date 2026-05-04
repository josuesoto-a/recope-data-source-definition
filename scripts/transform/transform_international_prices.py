import json
import csv
from pathlib import Path


def transform_to_csv(input_path: Path, output_path: Path):

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

    print(f"Rows written: {len(data)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":

    INPUT_PATH = Path(
        "data/processed/international_prices_cleaned.json"
    )

    OUTPUT_PATH = Path(
        "data/processed/international_prices.csv"
    )

    transform_to_csv(INPUT_PATH, OUTPUT_PATH)