import json
import csv
from pathlib import Path


def transform_consumer_prices(input_path: Path, output_path: Path):

    with open(input_path, "r") as file:
        data = json.load(file)

    if not data:
        raise ValueError("No data to transform")

    # Definir orden de columnas (importante en pipelines)
    fieldnames = [
        "date",
        "product",
        "price_crc",
        "tax_crc",
        "base_price_crc",
        "margin",
        "update_date",
        "product_id",
        "ingestion_timestamp"
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in data:
            writer.writerow(row)

    print("Transformation completed")
    print(f"Rows written: {len(data)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":

    INPUT_PATH = Path(
        "data/processed/consumer_prices_cleaned.json"
    )

    OUTPUT_PATH = Path(
        "data/processed/consumer_prices.csv"
    )

    transform_consumer_prices(INPUT_PATH, OUTPUT_PATH)