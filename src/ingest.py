"""Simulate the Lambda ingest step (local, no cloud).

Reads data/sample_311_requests.csv, validates required fields,
drops duplicates by unique_key, and writes
data/raw/311_requests_clean.csv. Prints row counts at each step.

Usage:
    python3 src/ingest.py
"""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "sample_311_requests.csv"
OUTPUT = BASE / "data" / "raw" / "311_requests_clean.csv"

REQUIRED = [
    "unique_key",
    "created_date",
    "complaint_type",
    "borough",
    "agency",
    "status",
]


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Input not found: {INPUT}. Run src/generate_sample_data.py first.")
    df = pd.read_csv(INPUT)
    input_rows = len(df)

    # Validate required fields: drop rows missing any required value.
    before_valid = len(df)
    df = df.dropna(subset=REQUIRED)
    df = df[(df["unique_key"].astype(str).str.strip() != "")]
    invalid_dropped = before_valid - len(df)

    # Drop duplicates by unique_key, keeping the first occurrence.
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["unique_key"], keep="first")
    duplicate_dropped = before_dedup - len(df)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    print(f"Input rows: {input_rows}")
    print(f"Invalid rows dropped: {invalid_dropped}")
    print(f"Duplicate rows dropped: {duplicate_dropped}")
    print(f"Output rows: {len(df)}")
    print(f"Wrote clean data to {OUTPUT}")


if __name__ == "__main__":
    main()
