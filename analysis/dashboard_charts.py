"""Create dashboard charts from the clean 311 data (pandas + matplotlib only).

Reads data/raw/311_requests_clean.csv (run src/ingest.py first) and writes:
    outputs/charts/requests_by_borough.png
    outputs/charts/requests_by_complaint_type_top10.png
    outputs/charts/requests_by_month.png

Usage:
    python3 analysis/dashboard_charts.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "raw" / "311_requests_clean.csv"
OUT_DIR = BASE / "outputs" / "charts"


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(
            f"Clean data not found: {INPUT}. Run src/ingest.py first."
        )
    df = pd.read_csv(INPUT, parse_dates=["created_date"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Requests by borough
    by_borough = df["borough"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    by_borough.plot(kind="bar", ax=ax)
    ax.set_title("311 Requests by Borough (synthetic sample)")
    ax.set_ylabel("Requests")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "requests_by_borough.png", dpi=150)
    plt.close(fig)

    # 2. Requests by complaint type, top 10
    by_type = df["complaint_type"].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    by_type.plot(kind="barh", ax=ax)
    ax.set_title("311 Requests by Complaint Type — Top 10 (synthetic sample)")
    ax.set_xlabel("Requests")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "requests_by_complaint_type_top10.png", dpi=150)
    plt.close(fig)

    # 3. Requests by month
    df["month"] = df["created_date"].dt.to_period("M").dt.to_timestamp()
    by_month = df.groupby("month").size().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    by_month.plot(kind="bar", ax=ax)
    ax.set_title("311 Requests by Month (synthetic sample)")
    ax.set_ylabel("Requests")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "requests_by_month.png", dpi=150)
    plt.close(fig)

    print(f"Input rows: {len(df)}")
    for name in [
        "requests_by_borough.png",
        "requests_by_complaint_type_top10.png",
        "requests_by_month.png",
    ]:
        path = OUT_DIR / name
        print(f"Wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
