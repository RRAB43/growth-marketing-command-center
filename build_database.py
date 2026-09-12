"""Load the three CSV files into a local SQLite database with no CLI required."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DB = ROOT / "marketing.db"

sources = {
    "marketing_ab": (DATA / "marketing_AB.csv", ","),
    "customers": (DATA / "marketing_campaign.csv", "\t"),
    "touchpoints": (DATA / "multi_touch_attribution_data.csv", ","),
}

with sqlite3.connect(DB) as connection:
    for table, (path, separator) in sources.items():
        print(f"Loading {path.name} -> {table}")
        frame = pd.read_csv(path, sep=separator)
        frame.to_sql(table, connection, if_exists="replace", index=False)
        print(f"  {len(frame):,} rows")

print(f"Created {DB}")
