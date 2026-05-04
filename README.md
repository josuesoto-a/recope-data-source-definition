# Recope Data Pipeline

## Overview

End-to-end data engineering pipeline that extracts, processes, and models fuel price data from RECOPE (Refinadora Costarricense de Petróleo).

The pipeline integrates multiple real-world data sources and produces a unified dataset ready for analysis.

---

## Data Sources

* Consumer Prices (local fuel prices in CRC)
* International Prices (reference prices in USD)
* Plantel Prices (bulk and industrial fuel prices)

All data is retrieved via REST APIs and stored in raw JSON format.

---

## Pipeline Architecture

The pipeline follows a standard data engineering workflow:

1. **Data Ingestion**

   * Fetch data from RECOPE APIs
   * Store raw JSON in `data/raw/`

2. **Data Cleaning**

   * Normalize field names
   * Parse dates and numeric values
   * Remove inconsistencies

3. **Data Transformation**

   * Convert JSON to tabular format (CSV)
   * Standardize schemas across sources

4. **Data Modeling**

   * Merge all datasets into a unified table
   * Normalize columns across sources

---

## Project Structure

```
recope-data-pipeline/

data/
    raw/
    processed/

scripts/
    fetch/
    transform/

README.md
requirements.txt
.gitignore
```

---

## Final Output

**File:**

```
data/processed/prices_modeled.csv
```

**Schema:**

* date
* product
* source
* price
* currency
* unit
* product_id
* ingestion_timestamp

---

## Tech Stack

* Python
* Requests
* JSON
* CSV
* Git / GitHub

---

## How to Run

```bash
# Fetch data
python scripts/fetch/fetch_consumer_prices.py
python scripts/fetch/fetch_international_prices.py
python scripts/fetch/fetch_plantel_prices.py

# Clean data
python scripts/transform/clean_consumer_prices.py
python scripts/transform/clean_international_prices.py
python scripts/transform/clean_plantel_prices.py

# Transform data
python scripts/transform/transform_consumer_prices.py
python scripts/transform/transform_international_prices.py
python scripts/transform/transform_plantel_prices.py

# Build final dataset
python scripts/transform/model_prices_data.py
```

---

## Future Improvements

* Add pipeline orchestration (Airflow / Prefect)
* Implement logging system
* Add unit and data quality tests
* Load data into a database (PostgreSQL / BigQuery)
* Automate scheduling

---
