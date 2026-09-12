-- Campaign response analysis (SQLite)
-- The six campaign columns are separate historical campaign outcomes.

-- 1. Acceptance rate by campaign
SELECT 'Campaign 1' AS campaign, SUM(AcceptedCmp1) AS acceptances, ROUND(100.0*AVG(AcceptedCmp1),2) AS acceptance_rate_pct FROM customers
UNION ALL SELECT 'Campaign 2', SUM(AcceptedCmp2), ROUND(100.0*AVG(AcceptedCmp2),2) FROM customers
UNION ALL SELECT 'Campaign 3', SUM(AcceptedCmp3), ROUND(100.0*AVG(AcceptedCmp3),2) FROM customers
UNION ALL SELECT 'Campaign 4', SUM(AcceptedCmp4), ROUND(100.0*AVG(AcceptedCmp4),2) FROM customers
UNION ALL SELECT 'Campaign 5', SUM(AcceptedCmp5), ROUND(100.0*AVG(AcceptedCmp5),2) FROM customers
UNION ALL SELECT 'Campaign 6', SUM(Response), ROUND(100.0*AVG(Response),2) FROM customers;

-- 2. Campaign 6 response by education (descriptive; assignment is unknown)
SELECT Education, COUNT(*) AS customers, SUM(Response) AS responders,
       ROUND(100.0*AVG(Response),2) AS response_rate_pct
FROM customers
GROUP BY Education
ORDER BY response_rate_pct DESC;

-- 3. Responders vs non-responders: recorded spend
WITH customer_spend AS (
    SELECT ID, Response,
           MntWines + MntFruits + MntMeatProducts + MntFishProducts
           + MntSweetProducts + MntGoldProds AS total_spend
    FROM customers
)
SELECT Response, COUNT(*) AS customers,
       ROUND(AVG(total_spend),2) AS avg_spend,
       SUM(total_spend) AS total_spend
FROM customer_spend
GROUP BY Response;

-- 4. Channel mix by income quartile; exclude missing and extreme income values
WITH valid_income AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY CAST(Income AS REAL)) AS income_quartile
    FROM customers
    WHERE Income IS NOT NULL AND Income <> '' AND CAST(Income AS REAL) <= 200000
)
SELECT income_quartile, COUNT(*) AS customers,
       ROUND(AVG(NumWebPurchases),2) AS avg_web_purchases,
       ROUND(AVG(NumCatalogPurchases),2) AS avg_catalog_purchases,
       ROUND(AVG(NumStorePurchases),2) AS avg_store_purchases
FROM valid_income
GROUP BY income_quartile
ORDER BY income_quartile;

