import json
from datetime import datetime
from pathlib import Path

from scripts.utils.logger import get_logger

logger = get_logger("clean_consumer_prices")


def clean_consumer_prices(input_path: Path, output_path: Path) -> None:
    """
    Clean consumer fuel price data.
    """

    try:
        logger.info(f"Starting cleaning | input={input_path}")

        with open(input_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        cleaned_data = []
        errors = 0

        for i, record in enumerate(raw_data):

            try:
                cleaned_record = {
                    "date": datetime.strptime(
                        record["fecha"], "%Y%m%d"
                    ).strftime("%Y-%m-%d"),

                    "product": record["nomprod"].split("(")[0].strip(),

                    "price_crc": float(record["preciototal"].strip()),

                    "tax_crc": float(record["impuesto"].strip()),

                    "base_price_crc": float(record["precsinimp"].strip()),

                    "margin": float(record["margenpromedio"].strip()),

                    "update_date": datetime.strptime(
                        record["fechaupd"], "%Y/%m/%d"
                    ).strftime("%Y-%m-%d"),

                    "product_id": record["id"],

                    "ingestion_timestamp": datetime.utcnow().isoformat()
                }

                cleaned_data.append(cleaned_record)

            except Exception as e:
                errors += 1
                logger.warning(
                    f"Record skipped | index={i} | error={e} | record={record}"
                )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

        logger.info(
            f"Cleaning completed | output={output_path} | "
            f"processed={len(cleaned_data)} | errors={errors}"
        )

    except Exception as e:
        logger.exception(f"Fatal error in clean_consumer_prices: {e}")
        raise


if __name__ == "__main__":

    from pathlib import Path

    RAW_DIR = "data/raw"

    # Solo para ejecución standalone
    files = list(Path(RAW_DIR).glob("consumer_prices*.json"))
    latest_file = max(files, key=lambda f: f.stat().st_mtime)

    OUTPUT_PATH = Path("data/processed/consumer_prices_cleaned.json")

    clean_consumer_prices(latest_file, OUTPUT_PATH)