"""Build RFM segments and campaign-response summaries."""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "marketing_campaign.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

SPEND = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
PURCHASES = ["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]
CAMPAIGNS = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"]


def score(series, higher_is_better=True):
    ranked = series.rank(method="first", ascending=True)
    labels = [1, 2, 3, 4, 5] if higher_is_better else [5, 4, 3, 2, 1]
    return pd.qcut(ranked, 5, labels=labels).astype(int)


def segment(row):
    r, f, m = row.r_score, row.f_score, row.m_score
    if r >= 4 and f >= 4 and m >= 4: return "Champions"
    if r >= 4 and f >= 3: return "Loyal"
    if r >= 4 and f <= 2: return "New / Promising"
    if r <= 2 and f >= 4: return "At Risk"
    if r <= 2 and m >= 4: return "Can't Lose Them"
    if r <= 2: return "Hibernating"
    return "Needs Attention"


def main():
    df = pd.read_csv(DATA, sep="\t")
    checks = {
        "rows": int(len(df)), "duplicate_customer_ids": int(df.ID.duplicated().sum()),
        "missing_income": int(df.Income.isna().sum()),
        "birth_year_below_1940": int((df.Year_Birth < 1940).sum()),
        "income_above_200000": int((df.Income > 200000).sum()),
    }
    df["recency"] = df.Recency
    df["frequency"] = df[PURCHASES].sum(axis=1)
    df["monetary"] = df[SPEND].sum(axis=1)
    df["r_score"] = score(df.recency, higher_is_better=False)
    df["f_score"] = score(df.frequency)
    df["m_score"] = score(df.monetary)
    df["segment"] = df.apply(segment, axis=1)
    rfm = df[["ID", "recency", "frequency", "monetary", "r_score", "f_score", "m_score", "segment"]]
    rfm.to_csv(OUT / "rfm_segments.csv", index=False)

    segment_summary = df.groupby("segment").agg(
        customers=("ID", "nunique"), avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"), total_spend=("monetary", "sum"),
        campaign_6_response_rate=("Response", "mean")).reset_index()
    segment_summary["customer_share_pct"] = segment_summary.customers / segment_summary.customers.sum() * 100
    segment_summary["spend_share_pct"] = segment_summary.total_spend / segment_summary.total_spend.sum() * 100
    segment_summary = segment_summary.sort_values("total_spend", ascending=False)
    segment_summary.to_csv(OUT / "segment_summary.csv", index=False)

    campaign_summary = pd.DataFrame({
        "campaign": ["Campaign 1", "Campaign 2", "Campaign 3", "Campaign 4", "Campaign 5", "Campaign 6"],
        "acceptances": [int(df[c].sum()) for c in CAMPAIGNS],
        "acceptance_rate_pct": [round(df[c].mean() * 100, 2) for c in CAMPAIGNS],
    })
    campaign_summary.to_csv(OUT / "campaign_summary.csv", index=False)

    top = segment_summary.iloc[0]
    metrics = {
        "data_checks": checks,
        "top_segment_by_spend": top.segment,
        "top_segment_customer_share_pct": round(float(top.customer_share_pct), 1),
        "top_segment_spend_share_pct": round(float(top.spend_share_pct), 1),
        "best_campaign": campaign_summary.loc[campaign_summary.acceptance_rate_pct.idxmax(), "campaign"],
        "best_campaign_acceptance_rate_pct": float(campaign_summary.acceptance_rate_pct.max()),
        "limitations": [
            "RFM labels are rule-based prioritization aids, not causal targeting effects.",
            "Income is not imputed for segmentation; outliers are reported and excluded only from income-specific analysis.",
            "Spend fields are treated as dataset monetary units because no currency is specified.",
        ],
    }
    (OUT / "segmentation_results.json").write_text(json.dumps(metrics, indent=2))
    print(segment_summary.round(2).to_string(index=False))
    print(f"Outputs written to {OUT}")


if __name__ == "__main__": main()
