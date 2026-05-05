from pathlib import Path

# FETCH
from scripts.fetch.fetch_consumer_prices import fetch_consumer_prices
from scripts.fetch.fetch_international_prices import fetch_international_prices
from scripts.fetch.fetch_plantel_prices import fetch_plantel_prices

# CLEAN
from scripts.transform.clean_consumer_prices import clean_consumer_prices
from scripts.transform.clean_international_prices import clean_international_prices
from scripts.transform.clean_plantel_prices import clean_plantel_prices

# TRANSFORM
from scripts.transform.transform_consumer_prices import transform_consumer_prices
from scripts.transform.transform_international_prices import transform_international_prices
from scripts.transform.transform_plantel_prices import transform_plantel_prices

# MODEL
from scripts.transform.model_prices_data import model_prices_data


# -----------------------------
# UTILIDAD: obtener último archivo
# -----------------------------
def get_latest_file(directory, pattern):
    files = list(Path(directory).glob(pattern))

    if not files:
        raise FileNotFoundError(f"No files found for pattern: {pattern}")

    return max(files, key=lambda f: f.stat().st_mtime)


# -----------------------------
# PIPELINE
# -----------------------------
def run_pipeline():

    print("Starting pipeline...\n")

    # -----------------------------
    # 1. FETCH
    # -----------------------------
    fetch_consumer_prices()
    fetch_international_prices()
    fetch_plantel_prices()

    # -----------------------------
    # 2. CLEAN
    # -----------------------------
    consumer_raw = get_latest_file("data/raw", "consumer_prices_*.json")
    international_raw = get_latest_file("data/raw", "international_prices_*.json")
    plantel_raw = get_latest_file("data/raw", "plantel_prices_*.json")

    consumer_clean = Path("data/processed/consumer_prices_cleaned.json")
    international_clean = Path("data/processed/international_prices_cleaned.json")
    plantel_clean = Path("data/processed/plantel_prices_cleaned.json")

    clean_consumer_prices(consumer_raw, consumer_clean)
    clean_international_prices(international_raw, international_clean)
    clean_plantel_prices(plantel_raw, plantel_clean)

    # -----------------------------
    # 3. TRANSFORM
    # -----------------------------
    consumer_csv = Path("data/processed/consumer_prices.csv")
    international_csv = Path("data/processed/international_prices.csv")
    plantel_csv = Path("data/processed/plantel_prices.csv")

    transform_consumer_prices(consumer_clean, consumer_csv)
    transform_international_prices(international_clean, international_csv)
    transform_plantel_prices(plantel_clean, plantel_csv)

    # -----------------------------
    # 4. MODEL (dataset final)
    # -----------------------------
    modeled_output = Path("data/processed/prices_modeled.csv")

    model_prices_data(
        consumer_csv,
        international_csv,
        plantel_csv,
        modeled_output
    )

    print("\nPipeline completed successfully.")


# -----------------------------
# ENTRYPOINT
# -----------------------------
if __name__ == "__main__":
    run_pipeline()