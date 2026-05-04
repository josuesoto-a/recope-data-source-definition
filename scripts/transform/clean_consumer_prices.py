import json
from datetime import datetime
from pathlib import Path


def get_latest_file(directory: str, pattern: str = "consumer_prices*.json") -> Path:
    """
    Return the most recently modified file matching the pattern inside directory.
    """
    files = list(Path(directory).glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No files found in {directory} matching {pattern}"
        )

    # Select file with latest modification time
    latest_file = max(files, key=lambda f: f.stat().st_mtime)

    return latest_file


def clean_consumer_prices(input_path: Path, output_path: Path) -> None:
    """
    Clean consumer fuel price data.

    Steps:
    1. Read raw JSON
    2. Normalize schema
    3. Convert types
    4. Save cleaned data
    """

    with open(input_path, "r") as file:
        raw_data = json.load(file)

    cleaned_data = []

    for record in raw_data:
        try:
            cleaned_record = {

                "date":
                    datetime.strptime(
                        record["fecha"], "%Y%m%d"
                    ).strftime("%Y-%m-%d"),

                "product":
                    record["nomprod"].split("(")[0].strip(),

                "price_crc":
                    float(record["preciototal"].strip()),

                "tax_crc":
                    float(record["impuesto"].strip()),

                "base_price_crc":
                    float(record["precsinimp"].strip()),

                "margin":
                    float(record["margenpromedio"].strip()),

                "update_date":
                    datetime.strptime(
                        record["fechaupd"], "%Y/%m/%d"
                    ).strftime("%Y-%m-%d"),

                "product_id":
                    record["id"],

                "ingestion_timestamp":
                    datetime.utcnow().isoformat()
            }

            cleaned_data.append(cleaned_record)

        except Exception as e:
            print(f"Skipping record due to error: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Cleaning completed")
    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Records processed: {len(cleaned_data)}")


if __name__ == "__main__":

    RAW_DIR = "data/raw"

    latest_file = get_latest_file(RAW_DIR)

    OUTPUT_PATH = Path(
        "data/processed/consumer_prices_cleaned.json"
    )

    clean_consumer_prices(
        latest_file,
        OUTPUT_PATH
    )