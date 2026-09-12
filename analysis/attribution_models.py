"""Compare first-touch, last-touch, and linear attribution models."""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "multi_touch_attribution_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def main():
    df = pd.read_csv(DATA).rename(columns=lambda c: c.strip().lower().replace(" ", "_"))
    df["timestamp"] = pd.to_datetime(df.timestamp, errors="raise")
    df["is_conversion"] = df.conversion.str.lower().eq("yes")
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)

    # Define a journey as all touches up to and including a user's first conversion.
    # Users without a conversion are retained for funnel reporting but receive no credit.
    first_conversion = (
        df.loc[df.is_conversion].groupby("user_id").timestamp.min().rename("first_conversion_at"))
    journeys = df.merge(first_conversion, on="user_id", how="inner")
    journeys = journeys[journeys.timestamp <= journeys.first_conversion_at].copy()
    converting_users = journeys.user_id.nunique()

    first = journeys.groupby("user_id", sort=False).first().channel.value_counts().rename("first_touch_credit")
    last = journeys.groupby("user_id", sort=False).last().channel.value_counts().rename("last_touch_credit")
    journeys["linear_credit"] = 1 / journeys.groupby("user_id").channel.transform("count")
    linear = journeys.groupby("channel").linear_credit.sum().rename("linear_credit")

    comparison = pd.concat([first, last, linear], axis=1).fillna(0)
    for col in comparison.columns:
        comparison[col.replace("credit", "share_pct")] = comparison[col] / comparison[col].sum() * 100
    comparison.index.name = "channel"
    comparison = comparison.reset_index().sort_values("linear_share_pct", ascending=False)
    comparison.to_csv(OUT / "attribution_comparison.csv", index=False)

    channel_funnel = df.groupby("channel").agg(
        touches=("user_id", "size"), unique_users=("user_id", "nunique"),
        conversion_events=("is_conversion", "sum")).reset_index()
    channel_funnel.to_csv(OUT / "channel_funnel.csv", index=False)

    delta = comparison.assign(
        last_vs_linear_pp=comparison.last_touch_share_pct - comparison.linear_share_pct)
    most_over = delta.loc[delta.last_vs_linear_pp.idxmax()]
    most_under = delta.loc[delta.last_vs_linear_pp.idxmin()]
    metrics = {
        "rows": int(len(df)), "unique_users": int(df.user_id.nunique()),
        "converting_users": int(converting_users),
        "journey_rule": "Touches through the user's first recorded conversion",
        "most_overcredited_by_last_touch": {
            "channel": most_over.channel, "difference_pp": round(float(most_over.last_vs_linear_pp), 2)},
        "most_undercredited_by_last_touch": {
            "channel": most_under.channel, "difference_pp": round(float(most_under.last_vs_linear_pp), 2)},
        "limitations": [
            "The file covers roughly two days and is suitable for model comparison, not budget forecasting.",
            "Attribution assigns descriptive credit; it does not estimate incremental causal impact.",
            "Repeated conversion flags are handled by ending each journey at the first conversion.",
        ],
    }
    (OUT / "attribution_results.json").write_text(json.dumps(metrics, indent=2))
    print(comparison[["channel", "first_touch_share_pct", "last_touch_share_pct", "linear_share_pct"]].round(2).to_string(index=False))
    print(f"Outputs written to {OUT}")


if __name__ == "__main__": main()
