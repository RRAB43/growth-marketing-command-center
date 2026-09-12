"""Generate a deterministic, source-linked weekly executive brief.

No API key is required. Python owns every number. The optional AI workflow in
ai-automation/README.md can improve the narrative without recomputing metrics.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def load(name):
    path = OUT / name
    if not path.exists():
        raise FileNotFoundError(f"Run the analysis modules first; missing {path}")
    return json.loads(path.read_text())


def main():
    ab = load("ab_test_results.json")
    seg = load("segmentation_results.json")
    att = load("attribution_results.json")
    p = ab["p_value"]
    p_text = "<0.001" if p < 0.001 else f"{p:.3f}"
    brief = f"""# Weekly Growth Analytics Brief

## BLUF
The ad treatment converted at **{ab['ad']['rate_pct']:.3f}%**, compared with **{ab['control']['rate_pct']:.3f}%** for the PSA control: a **{ab['relative_uplift_pct']:.1f}% relative uplift** ({ab['absolute_lift_pp']:.3f} percentage points; p {p_text}). The immediate recommendation is to validate experiment assignment and instrumentation, then use the effect-size range—not significance alone—to inform rollout economics.

## Experiment decision
- Ad group: **{ab['ad']['conversions']:,} conversions / {ab['ad']['users']:,} users**.
- PSA control: **{ab['control']['conversions']:,} conversions / {ab['control']['users']:,} users**.
- 95% confidence interval for absolute lift: **{ab['ci_95_difference_pp'][0]:.3f} to {ab['ci_95_difference_pp'][1]:.3f} pp**.
- At an illustrative value of **${ab['scenario_value_per_conversion']} per conversion**, the observed effect corresponds to approximately **${ab['scenario_incremental_value']:,}** across the ad-group population. This is a scenario, not measured revenue.

## Audience prioritization
- **{seg['top_segment_by_spend']}** is the largest segment by recorded spend, representing **{seg['top_segment_customer_share_pct']:.1f}% of customers** and **{seg['top_segment_spend_share_pct']:.1f}% of spend**.
- Test differentiated retention or upsell messaging for this segment; measure incremental response against a randomized holdout.
- **{seg['best_campaign']}** had the highest observed acceptance rate at **{seg['best_campaign_acceptance_rate_pct']:.2f}%**. Campaign comparisons are descriptive because assignment rules are unavailable.

## Measurement risk
- Under last-touch attribution, **{att['most_overcredited_by_last_touch']['channel']}** receives **{att['most_overcredited_by_last_touch']['difference_pp']:.2f} pp more credit** than under a linear model.
- **{att['most_undercredited_by_last_touch']['channel']}** receives **{abs(att['most_undercredited_by_last_touch']['difference_pp']):.2f} pp less credit** under last touch than linear.
- Do not interpret either model as incrementality. Use attribution for journey reporting and controlled experiments or geo tests for causal budget decisions.

## Next actions
1. Validate randomization, sample-ratio imbalance, event definitions and tracking completeness.
2. Translate the A/B confidence interval into downside/base/upside unit economics using real margin per conversion.
3. Run one segment-level campaign with a holdout group and predefined success and guardrail metrics.
4. Report attribution-model sensitivity beside channel results so leadership sees how the credit rule changes the conclusion.

## Limitations
- The three public datasets describe different populations and must not be joined at the user level.
- Segmentation and attribution findings are descriptive, not causal.
- The attribution file spans roughly two days; it demonstrates measurement sensitivity rather than long-term channel performance.
"""
    (ROOT / "WEEKLY_BRIEF.md").write_text(brief)
    print(f"Created {ROOT / 'WEEKLY_BRIEF.md'}")


if __name__ == "__main__": main()
