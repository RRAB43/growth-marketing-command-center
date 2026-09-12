-- RFM segmentation (SQLite)
-- Lower recency is better; higher frequency and monetary values are better.

WITH rfm_base AS (
    SELECT
        ID,
        CAST(Recency AS INTEGER) AS recency,
        NumWebPurchases + NumCatalogPurchases + NumStorePurchases AS frequency,
        MntWines + MntFruits + MntMeatProducts + MntFishProducts
        + MntSweetProducts + MntGoldProds AS monetary
    FROM customers
),
rfm_scores AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency DESC, ID) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC, ID) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, ID) AS m_score
    FROM rfm_base
),
segmented AS (
    SELECT *,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 4 AND f_score >= 3 THEN 'Loyal'
            WHEN r_score >= 4 AND f_score <= 2 THEN 'New / Promising'
            WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk'
            WHEN r_score <= 2 AND m_score >= 4 THEN 'Can''t Lose Them'
            WHEN r_score <= 2 THEN 'Hibernating'
            ELSE 'Needs Attention'
        END AS segment
    FROM rfm_scores
),
totals AS (
    SELECT SUM(monetary) AS all_spend FROM segmented
)
SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM segmented), 1) AS customer_share_pct,
    ROUND(AVG(recency), 1) AS avg_recency,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    SUM(monetary) AS total_spend,
    ROUND(100.0 * SUM(monetary) / totals.all_spend, 1) AS spend_share_pct,
    CASE
        WHEN segment = 'Champions' THEN 'Referral and early-access test'
        WHEN segment = 'Loyal' THEN 'Cross-sell personalization test'
        WHEN segment = 'New / Promising' THEN 'Second-purchase onboarding test'
        WHEN segment = 'At Risk' THEN 'Randomized win-back offer'
        WHEN segment = 'Can''t Lose Them' THEN 'High-value service recovery'
        WHEN segment = 'Hibernating' THEN 'Low-cost reactivation test'
        ELSE 'Collect preference signals'
    END AS recommended_test
FROM segmented
CROSS JOIN totals
GROUP BY segment, totals.all_spend
ORDER BY total_spend DESC;

