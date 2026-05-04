import json
from datetime import datetime
from pathlib import Path


def get_latest_file(directory: str, pattern: str = "plantel_prices*.json") -> Path:

    files = list(Path(directory).glob(pattern))

    if not files:
        raise FileNotFoundError("No plantel price files found")

    return max(files, key=lambda f: f.stat().st_mtime)


def format_date(date_str, fmt):
    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")


def clean_plantel_prices(input_path: Path, output_path: Path):

    with open(input_path, "r") as file:
        raw_data = json.load(file)

    cleaned_data = []

    for record in raw_data:

        try:
            cleaned_record = {

                "date":
                    format_date(record["fecha"], "%Y%m%d"),

                "product":
                    record["nomprod"].split("(")[0].strip(),

                "price_crc":
                    float(record["preciototal"].strip()),

                "tax_crc":
                    float(record["impuesto"].strip()),

                "base_price_crc":
                    float(record["precsinimp"].strip()),

                "unit":
                    record["tipo"],

                "product_id":
                    record["id"],

                "update_date":
                    format_date(record["fechaupd"], "%Y/%m/%d"),

                "source":
                    "plantel",

                "ingestion_timestamp":
                    datetime.utcnow().isoformat()
            }

            cleaned_data.append(cleaned_record)

        except Exception as e:
            print(f"Skipping record: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Records processed: {len(cleaned_data)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":

    RAW_DIR = "data/raw"

    latest_file = get_latest_file(RAW_DIR)

    OUTPUT_PATH = Path(
        "data/processed/plantel_prices_cleaned.json"
    )

    clean_plantel_prices(latest_file, OUTPUT_PATH)