# Kaggle E-Commerce Data Warehouse Dataset

## Source

Dataset: E-Commerce Data Warehouse Dataset  
Source: Kaggle  
Author: shandeep777  
Link: https://www.kaggle.com/datasets/shandeep777/e-commerce-data-warehouse-dataset  
Licence: Apache License 2.0

## Purpose in Demand Weaver

This dataset is used as the internal e-commerce data source for the Demand Weaver mock data project.

It provides structured sample data for testing:

- CSV ingestion
- DuckDB loading
- product and order analysis
- basic data modelling
- later orchestration with Dagster

## Dataset context

The dataset is synthetic/sample e-commerce data structured in a data warehouse format. It includes dimension and fact tables covering products, customers, orders, returns, marketing, fulfilment and locations.

The dataset is based around the Indian market, including Indian locations, phone formats and payment methods such as UPI.

## Files used in the PoC

For the initial PoC, only the following files are required:

- `DIM_PRODUCT.csv`
- `FACT_ORDERS.csv`
- `DIM_CALENDAR.csv`

These tables are enough to validate product-level revenue analysis over time.

## Important notes

- Some tables contain PII-like sample fields, such as emails, phone numbers, UPI IDs and bank details.
- PII fields should not be used in public outputs.
- `FACT_ORDERS.date_id` is stored as a `YYYY-MM-DD` string, while other fact tables may use `YYYYMMDD` integer date keys.
- Date fields may need casting before joins.
- This folder is used for raw source files only. Transformed outputs should go in `data/processed/`.
- Some source files (e.g. FACT_ORDERS.csv) exceed GitHub’s 100MB file size limit.
- Full datasets should be stored locally or externally and are not fully version-controlled in this repository.

## Attribution

This project uses data from the Kaggle dataset listed above. No endorsement by the original author is implied.


## Data Storage (DuckDB)

The project uses DuckDB as a local analytical database.

- The database file is stored at: `data/processed/demand_weaver.duckdb`
- Tables are created from CSV files via an ingestion script
- Only a subset of the dataset is loaded for the POC

### Notes
- DuckDB CLI may require manual installation in some environments
- Large raw datasets are not fully stored in the repository due to GitHub size limits