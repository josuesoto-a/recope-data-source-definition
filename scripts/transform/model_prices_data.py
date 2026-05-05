import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
USD_TO_CRC = 540  # tipo de cambio base (puedes hacerlo dinámico luego)


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
        lambda row: row["price"] * USD_TO_CRC if row["currency"] == "USD" else row["price"],
        axis=1
    )
    return df


# -----------------------------
# MODELING
# -----------------------------
def model_prices_data(
    consumer_path,
    international_path,
    plantel_path,
    output_path
):

    # -----------------------------
    # Cargar datasets (CRÍTICO: product_id como string)
    # -----------------------------
    df_consumer = pd.read_csv(consumer_path, dtype={"product_id": str})
    df_international = pd.read_csv(international_path, dtype={"product_id": str})
    df_plantel = pd.read_csv(plantel_path, dtype={"product_id": str})

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
    # NORMALIZAR MONEDA
    # -----------------------------
    df_consumer_model = normalize_currency(df_consumer_model)
    df_international_model = normalize_currency(df_international_model)
    df_plantel_model = normalize_currency(df_plantel_model)

    # -----------------------------
    # Columnas finales
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
    # Validación de schema
    # -----------------------------
    for name, df in {
        "consumer": df_consumer_model,
        "international": df_international_model,
        "plantel": df_plantel_model
    }.items():

        missing = [col for col in common_cols if col not in df.columns]

        if missing:
            raise ValueError(f"{name} missing columns: {missing}")

    # -----------------------------
    # Selección de columnas
    # -----------------------------
    df_consumer_model = df_consumer_model[common_cols]
    df_international_model = df_international_model[common_cols]
    df_plantel_model = df_plantel_model[common_cols]

    # -----------------------------
    # Concatenación
    # -----------------------------
    df_final = pd.concat(
        [df_consumer_model, df_international_model, df_plantel_model],
        ignore_index=True
    )

    # -----------------------------
    # Guardar
    # -----------------------------
    df_final.to_csv(output_path, index=False)

    print("Modeling completed")
    print(f"Total rows: {len(df_final)}")
    print(f"Output: {output_path}")


# -----------------------------
# EJECUCIÓN MANUAL
# -----------------------------
if __name__ == "__main__":

    model_prices_data(
        "data/processed/consumer_prices.csv",
        "data/processed/international_prices.csv",
        "data/processed/plantel_prices.csv",
        "data/processed/prices_modeled.csv"
    )