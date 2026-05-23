import json
from datetime import datetime
from pathlib import Path

from scripts.utils.logger import get_logger

logger = get_logger("clean_international_prices")


def format_date(date_str):
    return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")


def clean_international_prices(input_path: Path, output_path: Path):
    """
    Clean international prices data.
    """

    try:
        logger.info(f"Starting cleaning | input={input_path}")

        with open(input_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        periodos = raw_data.get("periodos", [])
        materiales = raw_data.get("materiales", [])

        cleaned_data = []
        errors = 0

        for material_idx, material in enumerate(materiales):

            try:
                product = material["nomprod"].split("(")[0].strip()
                product_id = material["id"]
                precios = material.get("precios", [])

                for i, precio in enumerate(precios):

                    try:
                        periodo = periodos[i]

                        cleaned_record = {
                            "date_start": format_date(periodo["desde"]),
                            "date_end": format_date(periodo["hasta"]),
                            "product": product,
                            "price_usd": float(precio),
                            "product_id": product_id,
                            "currency": "USD",
                            "source": "international",
                            "ingestion_timestamp": datetime.utcnow().isoformat()
                        }

                        cleaned_data.append(cleaned_record)

                    except Exception as e:
                        errors += 1
                        logger.warning(
                            f"Record skipped | material_index={material_idx} | "
                            f"price_index={i} | error={e} | material={material}"
                        )

            except Exception as e:
                errors += 1
                logger.warning(
                    f"Material skipped | index={material_idx} | error={e} | material={material}"
                )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

        logger.info(
            f"Cleaning completed | output={output_path} | "
            f"processed={len(cleaned_data)} | errors={errors}"
        )

    except Exception as e:
        logger.exception(f"Fatal error in clean_international_prices: {e}")
        raise


if __name__ == "__main__":

    RAW_DIR = "data/raw"
    files = list(Path(RAW_DIR).glob("international_prices*.json"))
    latest_file = max(files, key=lambda f: f.stat().st_mtime)

    OUTPUT_PATH = Path("data/processed/international_prices_cleaned.json")

    clean_international_prices(latest_file, OUTPUT_PATH)