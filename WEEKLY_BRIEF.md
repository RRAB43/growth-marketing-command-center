# Weekly Growth Analytics Brief

## BLUF
The ad treatment converted at **2.555%**, compared with **1.785%** for the PSA control: a **43.1% relative uplift** (0.769 percentage points; p <0.001). The immediate recommendation is to validate experiment assignment and instrumentation, then use the effect-size range—not significance alone—to inform rollout economics.

## Experiment decision
- Ad group: **14,423 conversions / 564,577 users**.
- PSA control: **420 conversions / 23,524 users**.
- 95% confidence interval for absolute lift: **0.595 to 0.943 pp**.
- At an illustrative value of **$25 per conversion**, the observed effect corresponds to approximately **$108,575** across the ad-group population. This is a scenario, not measured revenue.

## Audience prioritization
- **At Risk** is the largest segment by recorded spend, representing **16.0% of customers** and **31.5% of spend**.
- Test differentiated retention or upsell messaging for this segment; measure incremental response against a randomized holdout.
- **Campaign 6** had the highest observed acceptance rate at **14.91%**. Campaign comparisons are descriptive because assignment rules are unavailable.

## Measurement risk
- Under last-touch attribution, **Social Media** receives **0.64 pp more credit** than under a linear model.
- **Search Ads** receives **0.60 pp less credit** under last touch than linear.
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
