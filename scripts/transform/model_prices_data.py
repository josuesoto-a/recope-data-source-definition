import csv
from pathlib import Path


def load_csv(path):
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)


def model_prices():

    base_path = Path("data/processed")

    consumer = load_csv(base_path / "consumer_prices.csv")
    international = load_csv(base_path / "international_prices.csv")
    plantel = load_csv(base_path / "plantel_prices.csv")

    modeled_data = []

    # --- CONSUMER ---
    for row in consumer:
        modeled_data.append({
            "date": row["date"],
            "product": row["product"],
            "source": "consumer",
            "price": float(row["price_crc"]),
            "currency": "CRC",
            "unit": "L",  # asumido (puedes refinar después)
            "product_id": row["product_id"],
            "ingestion_timestamp": row["ingestion_timestamp"]
        })

    # --- INTERNATIONAL ---
    for row in international:
        modeled_data.append({
            "date": row["date_start"],  # decisión: usar inicio del periodo
            "product": row["product"],
            "source": "international",
            "price": float(row["price_usd"]),
            "currency": "USD",
            "unit": None,
            "product_id": row["product_id"],
            "ingestion_timestamp": row["ingestion_timestamp"]
        })

    # --- PLANTEL ---
    for row in plantel:
        modeled_data.append({
            "date": row["date"],
            "product": row["product"],
            "source": "plantel",
            "price": float(row["price_crc"]),
            "currency": "CRC",
            "unit": row["unit"],
            "product_id": row["product_id"],
            "ingestion_timestamp": row["ingestion_timestamp"]
        })

    output_path = base_path / "prices_modeled.csv"

    with open(output_path, "w", newline="") as file:
        fieldnames = modeled_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(modeled_data)

    print(f"Modeled dataset created: {output_path}")
    print(f"Total rows: {len(modeled_data)}")


if __name__ == "__main__":
    model_prices()