import pandas as pd
from pathlib import Path

from scripts.utils.logger import get_logger

logger = get_logger("model_prices_data")

# -----------------------------
# CONFIG
# -----------------------------
USD_TO_CRC = 540


# -----------------------------
# UTILIDAD: asegurar columnas
# -----------------------------
def ensure_columns(df, defaults):
    for col, value in defaults.items():
        if col not in df.columns:
            df[col] = value
    return df


# -----------------------------
# NORMALIZAR MONEDA
# -----------------------------
def normalize_currency(df):
    df["price_crc"] = df.apply(
        lambda row: row["price"] * USD_TO_CRC
        if row["currency"] == "USD"
        else row["price"],
        axis=1
    )
    return df


# -----------------------------
# MODELING
# -----------------------------
def model_prices_data(
    consumer_path: Path,
    international_path: Path,
    plantel_path: Path,
    output_path: Path
):

    try:
        logger.info("Starting modeling process")

        # -----------------------------
        # LOAD
        # -----------------------------
        logger.info("Loading datasets")

        df_consumer = pd.read_csv(consumer_path, dtype={"product_id": str})
        df_international = pd.read_csv(international_path, dtype={"product_id": str})
        df_plantel = pd.read_csv(plantel_path, dtype={"product_id": str})

        logger.info(
            f"Datasets loaded | consumer={len(df_consumer)} | "
            f"international={len(df_international)} | plantel={len(df_plantel)}"
        )

        # -----------------------------
        # CONSUMER
        # -----------------------------
        df_consumer_model = df_consumer.rename(columns={
            "price_crc": "price"
        })

        df_consumer_model["currency"] = "CRC"

        df_consumer_model = ensure_columns(df_consumer_model, {
            "source": "consumer",
            "unit": "L"
        })

        df_consumer_model["price_unit"] = "CRC_per_L"

        # -----------------------------
        # INTERNATIONAL
        # -----------------------------
        df_international_model = df_international.rename(columns={
            "price_usd": "price",
            "date_start": "date"
        })

        df_international_model = ensure_columns(df_international_model, {
            "source": "international",
            "unit": None,
            "currency": "USD"
        })

        df_international_model["price_unit"] = "USD_unknown"

        # -----------------------------
        # PLANTEL
        # -----------------------------
        df_plantel_model = df_plantel.rename(columns={
            "price_crc": "price"
        })

        df_plantel_model["currency"] = "CRC"

        df_plantel_model = ensure_columns(df_plantel_model, {
            "source": "plantel"
        })

        df_plantel_model["price_unit"] = (
            df_plantel_model["currency"] + "_per_" +
            df_plantel_model["unit"].fillna("unknown")
        )

        # -----------------------------
        # NORMALIZACIÓN MONETARIA
        # -----------------------------
        logger.info("Normalizing currency")

        df_consumer_model = normalize_currency(df_consumer_model)
        df_international_model = normalize_currency(df_international_model)
        df_plantel_model = normalize_currency(df_plantel_model)

        # -----------------------------
        # COLUMNAS FINALES
        # -----------------------------
        common_cols = [
            "date",
            "product",
            "source",
            "price",
            "currency",
            "unit",
            "price_unit",
            "price_crc",
            "product_id",
            "ingestion_timestamp"
        ]

        # -----------------------------
        # VALIDACIÓN
        # -----------------------------
        for name, df in {
            "consumer": df_consumer_model,
            "international": df_international_model,
            "plantel": df_plantel_model
        }.items():

            missing = [col for col in common_cols if col not in df.columns]

            if missing:
                raise ValueError(f"{name} missing columns: {missing}")

        logger.info("Schema validation passed")

        # -----------------------------
        # SELECCIÓN
        # -----------------------------
        df_consumer_model = df_consumer_model[common_cols]
        df_international_model = df_international_model[common_cols]
        df_plantel_model = df_plantel_model[common_cols]

        # -----------------------------
        # CONCAT
        # -----------------------------
        logger.info("Concatenating datasets")

        df_final = pd.concat(
            [df_consumer_model, df_international_model, df_plantel_model],
            ignore_index=True
        )

        # -----------------------------
        # SAVE
        # -----------------------------
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df_final.to_csv(output_path, index=False)

        logger.info(
            f"Modeling completed | total_rows={len(df_final)} | output={output_path}"
        )

    except Exception as e:
        logger.exception(f"Error in model_prices_data: {e}")
        raise


# -----------------------------
# ENTRYPOINT
# -----------------------------
if __name__ == "__main__":

    model_prices_data(
        Path("data/processed/consumer_prices.csv"),
        Path("data/processed/international_prices.csv"),
        Path("data/processed/plantel_prices.csv"),
        Path("data/processed/prices_modeled.csv")
    )