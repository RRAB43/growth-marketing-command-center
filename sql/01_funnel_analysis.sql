-- Growth funnel analysis (SQLite)
-- Grain: one row per user. "converted" is stored as True/False text after CSV import.

-- 1. Conversion rate by experiment group
SELECT
    "test group" AS test_group,
    COUNT(*) AS users,
    SUM(CASE WHEN LOWER(CAST(converted AS TEXT)) IN ('true','1') THEN 1 ELSE 0 END) AS conversions,
    ROUND(100.0 * AVG(CASE WHEN LOWER(CAST(converted AS TEXT)) IN ('true','1') THEN 1.0 ELSE 0.0 END), 3) AS conversion_rate_pct
FROM marketing_ab
GROUP BY "test group";

-- 2. Descriptive conversion rate by exposure bucket
WITH bucketed AS (
    SELECT *,
        CASE
            WHEN CAST("total ads" AS INTEGER) <= 10 THEN '01-10'
            WHEN CAST("total ads" AS INTEGER) <= 25 THEN '11-25'
            WHEN CAST("total ads" AS INTEGER) <= 50 THEN '26-50'
            WHEN CAST("total ads" AS INTEGER) <= 100 THEN '51-100'
            ELSE '101+'
        END AS exposure_bucket
    FROM marketing_ab
)
SELECT
    exposure_bucket,
    "test group" AS test_group,
    COUNT(*) AS users,
    ROUND(100.0 * AVG(CASE WHEN LOWER(CAST(converted AS TEXT)) IN ('true','1') THEN 1.0 ELSE 0.0 END), 3) AS conversion_rate_pct
FROM bucketed
GROUP BY exposure_bucket, "test group"
ORDER BY exposure_bucket, test_group;

-- 3. Timing diagnostics; require at least 100 users to reduce noisy cells
SELECT
    "most ads day" AS most_ads_day,
    CAST("most ads hour" AS INTEGER) AS most_ads_hour,
    "test group" AS test_group,
    COUNT(*) AS users,
    ROUND(100.0 * AVG(CASE WHEN LOWER(CAST(converted AS TEXT)) IN ('true','1') THEN 1.0 ELSE 0.0 END), 3) AS conversion_rate_pct
FROM marketing_ab
GROUP BY "most ads day", "most ads hour", "test group"
HAVING COUNT(*) >= 100
ORDER BY conversion_rate_pct DESC;

-- Exposure and timing variables are post-assignment and should not be read causally.
