from pathlib import Path
import duckdb
import pandas as pd
from pytrends.request import TrendReq

DB_PATH = Path("data/processed/demand_weaver.duckdb")

KEYWORD = "mobile phones"
GEO = "IN"
TIMEFRAME = "today 12-m"

def main():
    print(f"Fetching Google Trends data for: {KEYWORD}")

    pytrends = TrendReq(hl="en-US", tz=330)
    pytrends.build_payload(
        kw_list=[KEYWORD],
        cat=0,
        timeframe=TIMEFRAME,
        geo=GEO,
        gprop=""
    )

    df = pytrends.interest_over_time().reset_index()

    if df.empty:
        raise ValueError("No Google Trends data returned.")

    df = df.rename(columns={
        "date": "trend_date",
        KEYWORD: "search_interest"
    })

    df["keyword"] = KEYWORD
    df["geo"] = GEO
    df["source"] = "google_trends"

    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    df = df[[
        "trend_date",
        "keyword",
        "geo",
        "search_interest",
        "source"
    ]]

    con = duckdb.connect(DB_PATH)
    con.register("google_trends_df", df)

    con.execute("""
        CREATE OR REPLACE TABLE google_trends_sample AS
        SELECT *
        FROM google_trends_df
    """)

    row_count = con.execute("SELECT COUNT(*) FROM google_trends_sample").fetchone()[0]

    con.close()

    print(f"Loaded google_trends_sample with {row_count} rows")

if __name__ == "__main__":
    main()