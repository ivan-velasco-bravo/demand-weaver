from pathlib import Path
import duckdb

RAW_DATA_DIR = Path("data/raw/keggles_ecomerce_dataset")
DB_PATH = Path("data/processed/demand_weaver.duckdb")

TABLES = {
    "dim_product": "DIM_PRODUCT.csv",
    "fact_orders": "FACT_ORDERS.csv",
    "dim_calendar": "DIM_CALENDAR.csv",
}

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(DB_PATH)

    for table_name, file_name in TABLES.items():
        csv_path = RAW_DATA_DIR / file_name

        print(f"Loading {file_name} into {table_name}...")

        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}', header=True)
        """)

        row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"{table_name}: {row_count:,} rows loaded")

    print(f"\nDuckDB database created at: {DB_PATH}")

    con.close()

if __name__ == "__main__":
    main()