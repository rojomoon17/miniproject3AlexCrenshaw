"""
Name:    Alex Crenshaw
Class:   INF601 - Advanced Programming in Python
Project: Mini Project 3 - Movie Ratings by Genre

Question: How does movie rating vary by genre, and has any genre's
average rating trended up or down by decade since the 1970s?

Fetches movies from the Practice Hub API and loads them into a Pandas
DataFrame.
"""

import os

import pandas as pd
import requests

API_BASE = "https://practice.fhsucyber.com"
API_TOKEN = os.environ.get("PRACTICE_API_TOKEN")
SAMPLE_SIZE = 500  # server max per request


def fetch_movies(sample_size=SAMPLE_SIZE):
    """Fetch a sample of movies from the Practice Hub API and return the
    raw list of row dicts."""
    if not API_TOKEN:
        raise SystemExit(
            "PRACTICE_API_TOKEN is not set. Set it to your Practice Hub "
            "API token before running this script."
        )

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"count": sample_size}
    try:
        resp = requests.get(
            f"{API_BASE}/api/v1/datasets/movies", headers=headers, params=params
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"Could not fetch movie data from the Practice Hub - {err}")

    return resp.json()["rows"]


def build_dataframe(rows):
    """Load the raw rows into a DataFrame and add a `decade` column
    derived from `year`."""
    df = pd.DataFrame(rows)
    df["decade"] = (df["year"] // 10) * 10
    return df


def main():
    rows = fetch_movies()
    df = build_dataframe(rows)

    print(f"Fetched {len(df)} movies from the Practice Hub.")
    print("Mean rating by genre:")
    print(df.groupby("genre")["rating"].mean().sort_values(ascending=False).round(2))


if __name__ == "__main__":
    main()
