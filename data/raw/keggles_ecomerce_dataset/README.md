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

## Attribution

This project uses data from the Kaggle dataset listed above. No endorsement by the original author is implied.