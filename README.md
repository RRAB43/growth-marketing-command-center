# Growth Marketing Command Center

An end-to-end portfolio case study across experimentation, customer segmentation, attribution-model sensitivity, executive reporting, and AI-ready workflow design. The project analyzes three public datasets containing 600K+ rows without falsely joining unrelated users across sources.

**Live dashboard:** add your GitHub Pages URL after publishing.

## Executive summary

- The ad treatment converted **2.555%** versus **1.785%** for the PSA control: **43.1% relative uplift** and **0.769 percentage-point absolute lift** (95% CI: 0.595–0.943 pp; p < 0.001).
- The **At Risk** RFM segment represents **16.0% of customers but 31.5% of recorded spend**, making a randomized win-back test the highest-priority segment action.
- Last-touch attribution gives **Social Media 0.64 pp more credit** than a linear model and **Search Ads 0.60 pp less**. The small but real shift demonstrates that the attribution rule changes the reported channel story.
- The three sources represent separate populations. They are analyzed as coordinated modules and are never joined at user level.

## Business questions

| Module | Decision |
|---|---|
| Experimentation | Did the ad treatment cause a detectable conversion lift, and is the effect large enough to evaluate economically? |
| Segmentation | Which customer groups deserve retention, upsell, or reactivation tests? |
| Attribution | How sensitive is channel credit to first-touch, last-touch, or linear rules? |
| Executive reporting | How can validated outputs become a repeatable leadership brief? |

## Reproducible workflow

```text
Raw public CSVs
      ↓
Validation + Python/SQL analysis
      ↓
Versioned CSV and JSON outputs
      ↓
Dashboard + deterministic weekly brief
      ↓
Optional browser-AI narrative review
```

Run everything from the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 build_database.py
python3 run_all.py
```

Successful completion ends with:

```text
All analyses completed. Review outputs/ and WEEKLY_BRIEF.md.
```

## Experiment design and verdict

The source contains one row per user and no missing values or duplicate user IDs. The treatment/control allocation is highly imbalanced (564,577 versus 23,524), so assignment integrity should be validated before rollout.

| Metric | PSA control | Ad treatment |
|---|---:|---:|
| Users | 23,524 | 564,577 |
| Conversions | 420 | 14,423 |
| Conversion rate | 1.785% | 2.555% |

The analysis uses a two-sided pooled two-proportion z-test and an unpooled 95% confidence interval for the absolute difference. A $25 value-per-conversion scenario suggests approximately $108.6K of incremental value across the treatment population, but this is explicitly a scenario because the dataset contains no revenue or cost field.

## RFM action framework

| Segment | Customer share | Spend share | Recommended next test |
|---|---:|---:|---|
| At Risk | 16.0% | 31.5% | Randomized win-back offer |
| Champions | 13.6% | 27.7% | Referral or early-access test |
| Needs Attention | 20.0% | 19.7% | Preference-data collection |
| Loyal | 10.0% | 9.4% | Cross-sell personalization |
| Hibernating | 21.6% | 5.2% | Low-cost reactivation |
| Can't Lose Them | 2.4% | 4.6% | High-value service recovery |
| New / Promising | 16.4% | 1.9% | Second-purchase onboarding |

These labels prioritize hypotheses; they do not prove that a particular intervention will work. Each recommendation should be tested against a holdout.

## Attribution judgment

A converting journey includes all recorded touches through the user's first conversion. The project compares first-touch, last-touch, and linear credit. It does not present attribution as incrementality: channel credit is a reporting rule, whereas causal budget allocation requires experiments, geo tests, or another identification strategy.

## Data-quality decisions

- Removed the CSV export index from the A/B file.
- Reported 24 missing income records, three birth years before 1940, and one income above 200,000.
- Excluded missing/extreme income only from income-quartile analysis; RFM does not require income.
- Ended attribution journeys at first conversion to handle users with repeated Yes/No event values.
- Preserved an as-of and limitation statement for every decision output.

## AI literacy without a paid API

Python deterministically computes all metrics. The optional workflow uses a version-controlled skill and browser-AI prompt to improve the narrative, while prohibiting the model from recomputing numbers. This separates calculation from language generation and keeps human review responsible for the final recommendation.

## Repository structure

```text
├── analysis/          # A/B testing, segmentation, attribution
├── sql/               # Reproducible business queries
├── outputs/           # Generated CSV and JSON evidence
├── dashboards/        # Standalone executive dashboard
├── ai-automation/     # Deterministic weekly brief workflow
├── data/              # Local raw files and source documentation
├── requirements.txt
├── build_database.py
├── run_all.py
└── WEEKLY_BRIEF.md
```

## Stack

Python · pandas · SciPy · SQL/SQLite · HTML/CSS · Chart.js · CLI automation · version-controlled AI skill

## Limitations

The public datasets do not describe the same company or user population. The A/B source does not provide randomization diagnostics, revenue, cost, or guardrail outcomes. The customer source does not document campaign assignment. The attribution source spans approximately two days. Findings are portfolio demonstrations and should not be treated as production decisions without validation.

## Interview framing

> I built a modular growth-measurement system across three public datasets. I kept the populations separate, validated each dataset at its own grain, quantified experiment lift and uncertainty, translated RFM segments into testable actions, demonstrated attribution-model sensitivity, and automated the executive readout without allowing AI to invent metrics.
