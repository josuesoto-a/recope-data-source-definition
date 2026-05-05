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
   * Introduce `price_unit` to resolve unit ambiguity
   * Normalize prices to CRC (`price_crc`)

---

## Project Structure

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

---

## Final Output

**File:**
data/processed/prices_modeled.csv

**Schema:**

* date
* product
* source
* price
* currency
* unit
* price_unit
* price_crc
* product_id
* ingestion_timestamp

---

## Current Status

Pipeline fully implemented:

* Data ingestion from 3 real-world sources
* Independent cleaning pipelines per source
* Data transformation to structured CSV format
* Unified data modeling across sources
* Currency normalization (CRC)
* Unit handling via `price_unit`
* End-to-end orchestration via `run_pipeline.py`

---

## Design Decisions

The modeled dataset includes multiple units (L, KG, PL) and currencies (CRC, USD).

At this stage:

* No physical unit conversion is applied (e.g., KG → L)
* International prices do not have a defined unit equivalence with local prices
* Currency normalization (USD → CRC) is applied, but unit comparability is not enforced

This design preserves data fidelity and avoids introducing incorrect assumptions.

**Implication:**

The dataset is suitable for:

* Data storage
* Exploration
* Auditing

But not yet for:

* Direct price comparison across all sources

---

## Pending Improvements

* Create analytics-ready dataset with comparable units (e.g., only `CRC_per_L`)
* Implement structured logging system
* Add data quality and unit tests
* Introduce orchestration tools (Airflow / Prefect)
* Automate scheduling (cron or workflow engine)

---

## Tech Stack

* Python
* Requests
* JSON
* CSV
* Pandas
* Git / GitHub

---

## How to Run

```bash
# Run full pipeline
python run_pipeline.py