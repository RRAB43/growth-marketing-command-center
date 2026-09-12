# Data — download instructions

CSVs are not committed to the repo (add `data/*.csv` to `.gitignore`). Download each dataset, place it here, keep these exact filenames:

| File to save here | Source | What it is |
|---|---|---|
| `marketing_AB.csv` | [Kaggle: Marketing A/B Testing](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing) | 588K users; columns: user id, test group (ad/psa), converted, total ads, most ads day, most ads hour |
| `marketing_campaign.csv` | [Kaggle: Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis) | 2,240 customers; demographics, spend by product category, responses to 6 campaigns. **Note: tab-separated** |
| `multi_touch_attribution_data.csv` | [Kaggle: Multi-Touch Attribution](https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution) | User journeys: touchpoints per user across channels with timestamps and conversion flags |

Downloading requires a free Kaggle account (Download button on each dataset page → unzip → rename as above).

## Loading into a database

From the repository root, use the included cross-platform loader:

```bash
python3 build_database.py
```

It creates `marketing.db` and loads the three sources as `marketing_ab`, `customers`, and `touchpoints`. The database is ignored by Git because it is reproducible from the source files.

Optional manual SQLite CLI path:

```bash
sqlite3 marketing.db
```

```sql
.mode csv
.import data/marketing_AB.csv marketing_ab
.separator "\t"
.import data/marketing_campaign.csv customers
.mode csv
.import data/multi_touch_attribution_data.csv touchpoints
```

If you prefer PostgreSQL (what the Apple repo used), `\copy` each file into staging tables — same table names.
