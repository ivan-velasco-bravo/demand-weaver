from pathlib import Path
import os

import duckdb
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path("data/processed/demand_weaver.duckdb")

KEYWORD = "mobile phones"
GEO = "IN"
DATE_RANGE = "today 12-m"

API_KEY = os.getenv("SERPAPI_API_KEY")

if not API_KEY:
    raise ValueError("SERPAPI_API_KEY is missing. Add it to your .env file.")


def fetch_google_trends():
    params = {
        "engine": "google_trends",
        "q": KEYWORD,
        "data_type": "TIMESERIES",
        "geo": GEO,
        "date": DATE_RANGE,
        "api_key": API_KEY,
    }

    last_error = None

    for attempt in range(3):
        try:
            print(f"SerpApi request attempt {attempt + 1}/3")

            response = requests.get(
                "https://serpapi.com/search.json",
                params=params,
                timeout=180,
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            last_error = error

            if attempt < 2:
                print(f"Request failed: {error}. Retrying...")
            else:
                print(f"Request failed: {error}. No retries left.")

    raise RuntimeError("SerpApi request failed after 3 attempts.") from last_error


def transform_response(data):
    timeline = data.get("interest_over_time", {}).get("timeline_data", [])

    if not timeline:
        raise ValueError("No timeline data returned from SerpApi.")

    rows = []

    for item in timeline:
        date_label = item.get("date")
        timestamp = item.get("timestamp")
        values = item.get("values", [])

        for value in values:
            rows.append(
                {
                    "trend_date_label": date_label,
                    "timestamp": timestamp,
                    "keyword": value.get("query", KEYWORD),
                    "geo": GEO,
                    "search_interest": value.get("extracted_value"),
                    "source": "serpapi_google_trends",
                }
            )

    return pd.DataFrame(rows)


def main():
    print(f"Fetching SerpApi Google Trends data for: {KEYWORD}")

    raw_data = fetch_google_trends()
    df = transform_response(raw_data)

    con = duckdb.connect(DB_PATH)
    con.register("serpapi_trends_df", df)

    con.execute(
        """
        CREATE OR REPLACE TABLE google_trends_sample AS
        SELECT *
        FROM serpapi_trends_df
        """
    )

    row_count = con.execute(
        "SELECT COUNT(*) FROM google_trends_sample"
    ).fetchone()[0]

    con.close()

    print(f"Loaded google_trends_sample with {row_count} rows")


if __name__ == "__main__":
    main()