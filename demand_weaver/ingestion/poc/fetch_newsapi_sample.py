from pathlib import Path
import os

import duckdb
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path("data/processed/demand_weaver.duckdb")

KEYWORD = "mobile phones"
LANGUAGE = "en"
PAGE_SIZE = 100

API_KEY = os.getenv("NEWSAPI_KEY")

if not API_KEY:
    raise ValueError("NEWSAPI_KEY is missing. Add it to your .env file.")


def fetch_news_articles():
    params = {
        "q": KEYWORD,
        "language": LANGUAGE,
        "sortBy": "publishedAt",
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY,
    }

    response = requests.get(
        "https://newsapi.org/v2/everything",
        params=params,
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def transform_response(data):
    articles = data.get("articles", [])

    if not articles:
        raise ValueError("No articles returned from NewsAPI.")

    rows = []

    for article in articles:
        source = article.get("source") or {}

        rows.append(
            {
                "keyword": KEYWORD,
                "source_id": source.get("id"),
                "source_name": source.get("name"),
                "author": article.get("author"),
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "source": "newsapi",
            }
        )

    return pd.DataFrame(rows)


def main():
    print(f"Fetching NewsAPI articles for: {KEYWORD}")

    raw_data = fetch_news_articles()
    df = transform_response(raw_data)

    con = duckdb.connect(DB_PATH)
    con.register("newsapi_df", df)

    con.execute(
        """
        CREATE OR REPLACE TABLE newsapi_sample AS
        SELECT *
        FROM newsapi_df
        """
    )

    row_count = con.execute(
        "SELECT COUNT(*) FROM newsapi_sample"
    ).fetchone()[0]

    con.close()

    print(f"Loaded newsapi_sample with {row_count} rows")


if __name__ == "__main__":
    main()