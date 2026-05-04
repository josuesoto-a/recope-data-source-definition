import json
from datetime import datetime
from pathlib import Path


def get_latest_file(directory: str, pattern: str = "international_prices*.json") -> Path:

    files = list(Path(directory).glob(pattern))

    if not files:
        raise FileNotFoundError("No international price files found")

    return max(files, key=lambda f: f.stat().st_mtime)


def format_date(date_str):
    return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")


def clean_international_prices(input_path: Path, output_path: Path):

    with open(input_path, "r") as file:
        raw_data = json.load(file)

    periodos = raw_data.get("periodos", [])
    materiales = raw_data.get("materiales", [])

    cleaned_data = []

    for material in materiales:

        product = material["nomprod"].split("(")[0].strip()
        product_id = material["id"]
        precios = material.get("precios", [])

        for i, precio in enumerate(precios):

            try:
                periodo = periodos[i]

                cleaned_record = {

                    "date_start":
                        format_date(periodo["desde"]),

                    "date_end":
                        format_date(periodo["hasta"]),

                    "product":
                        product,

                    "price_usd":
                        float(precio),

                    "product_id":
                        product_id,

                    "currency":
                        "USD",

                    "source":
                        "international",

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
        "data/processed/international_prices_cleaned.json"
    )

    clean_international_prices(latest_file, OUTPUT_PATH)