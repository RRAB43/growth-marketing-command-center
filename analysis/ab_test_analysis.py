"""Reproducible analysis of the Marketing A/B Testing dataset."""

from pathlib import Path
import json
import math
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "marketing_AB.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def proportion_test(success_a, total_a, success_b, total_b):
    """Two-sided pooled z-test and unpooled 95% CI for B minus A."""
    p_a, p_b = success_a / total_a, success_b / total_b
    pooled = (success_a + success_b) / (total_a + total_b)
    se_test = math.sqrt(pooled * (1 - pooled) * (1 / total_a + 1 / total_b))
    z = (p_b - p_a) / se_test
    p_value = 2 * norm.sf(abs(z))
    se_ci = math.sqrt(p_a * (1 - p_a) / total_a + p_b * (1 - p_b) / total_b)
    diff = p_b - p_a
    return z, p_value, diff - 1.96 * se_ci, diff + 1.96 * se_ci


def exposure_bucket(value):
    if value <= 10: return "01-10"
    if value <= 25: return "11-25"
    if value <= 50: return "26-50"
    if value <= 100: return "51-100"
    return "101+"


def main():
    df = pd.read_csv(DATA).rename(columns=lambda c: c.strip().lower().replace(" ", "_"))
    df = df.drop(columns=["unnamed:_0"], errors="ignore")
    checks = {
        "rows": int(len(df)), "unique_users": int(df.user_id.nunique()),
        "duplicate_user_ids": int(df.user_id.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "groups": sorted(df.test_group.unique().tolist()),
    }
    if checks["duplicate_user_ids"]: raise ValueError("Duplicate user IDs found.")
    if set(checks["groups"]) != {"ad", "psa"}: raise ValueError("Expected ad and psa groups.")

    summary = df.groupby("test_group", as_index=False).agg(
        users=("user_id", "nunique"), conversions=("converted", "sum"),
        conversion_rate=("converted", "mean"))
    summary["conversion_rate_pct"] = summary.conversion_rate * 100
    summary.to_csv(OUT / "ab_test_summary.csv", index=False)
    indexed = summary.set_index("test_group")
    control, treatment = indexed.loc["psa"], indexed.loc["ad"]
    z, p_value, ci_low, ci_high = proportion_test(
        int(control.conversions), int(control.users), int(treatment.conversions), int(treatment.users))
    absolute_lift = treatment.conversion_rate - control.conversion_rate
    relative_uplift = absolute_lift / control.conversion_rate
    incremental_conversions = absolute_lift * treatment.users

    df["exposure_bucket"] = df.total_ads.map(exposure_bucket)
    exposure = df.groupby(["exposure_bucket", "test_group"], observed=True).agg(
        users=("user_id", "nunique"), conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")).reset_index()
    exposure["conversion_rate_pct"] = exposure.conversion_rate * 100
    exposure.to_csv(OUT / "conversion_by_exposure.csv", index=False)

    timing = df.groupby(["most_ads_day", "most_ads_hour", "test_group"]).agg(
        users=("user_id", "nunique"), conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")).reset_index()
    timing["conversion_rate_pct"] = timing.conversion_rate * 100
    timing.to_csv(OUT / "conversion_by_day_hour.csv", index=False)

    value_per_conversion = 25
    results = {
        "data_checks": checks,
        "control": {"users": int(control.users), "conversions": int(control.conversions), "rate_pct": round(control.conversion_rate * 100, 3)},
        "ad": {"users": int(treatment.users), "conversions": int(treatment.conversions), "rate_pct": round(treatment.conversion_rate * 100, 3)},
        "absolute_lift_pp": round(absolute_lift * 100, 3),
        "relative_uplift_pct": round(relative_uplift * 100, 1),
        "z_statistic": round(z, 3), "p_value": p_value,
        "ci_95_difference_pp": [round(ci_low * 100, 3), round(ci_high * 100, 3)],
        "estimated_incremental_conversions_in_ad_group": round(incremental_conversions),
        "scenario_value_per_conversion": value_per_conversion,
        "scenario_incremental_value": round(incremental_conversions * value_per_conversion),
        "caveats": [
            "Group sizes are heavily imbalanced; random-assignment integrity cannot be verified from this file alone.",
            "Exposure timing and volume patterns are descriptive, not causal.",
            "The $25 value per conversion is a scenario because the dataset contains no revenue field.",
        ],
    }
    (OUT / "ab_test_results.json").write_text(json.dumps(results, indent=2))
    print(f"Ads: {treatment.conversion_rate*100:.3f}% | PSA: {control.conversion_rate*100:.3f}%")
    print(f"Relative uplift: {relative_uplift*100:.1f}% | absolute lift: {absolute_lift*100:.3f} pp | p={p_value:.3g}")
    print(f"95% CI: [{ci_low*100:.3f}, {ci_high*100:.3f}] pp")
    print(f"Outputs written to {OUT}")


if __name__ == "__main__": main()
