"""Generate deterministic synthetic NYC 311 sample data.

This is SYNTHETIC data for demonstration only. It is not the original
production data from the LinkedIn project, and no production metrics
(1M+ rows, 40+ tests, etc.) are claimed for this sample run.

Usage:
    python3 src/generate_sample_data.py
    # writes data/sample_311_requests.csv (900 rows, seed 42)
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
N_ROWS = 900
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "sample_311_requests.csv"

BOROUGHS = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]

# complaint_type -> (descriptor options, agency)
COMPLAINTS = {
    "Noise": (["Loud Music/Party", "Construction Noise", "Banging/Pounding"], "NYPD"),
    "Heat/Hot Water": (["No Heat", "No Hot Water", "Apartment Too Cold"], "HPD"),
    "Blocked Driveway": (["Blocked Driveway - No Access", "Partially Blocked Driveway"], "NYPD"),
    "Street Condition": (["Pothole", "Cave-in", "Failed Street Repair"], "DOT"),
    "Illegal Parking": (["Double Parked", "Blocked Hydrant", "Parking in Bike Lane"], "NYPD"),
    "Street Light Condition": (["Street Light Out", "Street Light Cycling"], "DOT"),
    "Sewer": (["Catch Basin Clogged", "Sewer Backup"], "DEP"),
    "Water System": (["Low Water Pressure", "Water Leak"], "DEP"),
    "Rodent": (["Rat Sighting", "Mouse Sighting"], "DOHMH"),
    "Missed Collection": (["Missed Recycling", "Missed Trash Collection"], "DSNY"),
}

STATUSES = ["Closed", "Closed", "Closed", "Open", "In Progress"]


def main() -> None:
    rng = random.Random(SEED)
    start = datetime(2026, 1, 1)
    rows = []
    for i in range(N_ROWS):
        complaint = rng.choice(list(COMPLAINTS.keys()))
        descriptors, agency = COMPLAINTS[complaint]
        created = start + timedelta(
            days=rng.randrange(0, 180),
            hours=rng.randrange(0, 24),
            minutes=rng.randrange(0, 60),
        )
        status = rng.choice(STATUSES)
        closed = ""
        if status == "Closed":
            closed_dt = created + timedelta(days=rng.randrange(0, 15))
            closed = closed_dt.strftime("%Y-%m-%d %H:%M:%S")
        rows.append(
            {
                "unique_key": 10000000 + i,
                "created_date": created.strftime("%Y-%m-%d %H:%M:%S"),
                "closed_date": closed,
                "complaint_type": complaint,
                "descriptor": rng.choice(descriptors),
                "borough": rng.choice(BOROUGHS),
                "agency": agency,
                "status": status,
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "unique_key",
        "created_date",
        "closed_date",
        "complaint_type",
        "descriptor",
        "borough",
        "agency",
        "status",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic rows to {OUTPUT}")


if __name__ == "__main__":
    main()
