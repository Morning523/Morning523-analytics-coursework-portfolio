-- ================================================================
-- Q4A  Cancellation Rate by Subscription Stage
-- ----------------------------------------------------------------
-- What it does : Maps each cancellation to the delivery cycle
--               it followed (1st box, 2nd box, etc.) and shows
--               what percentage of all cancellations each stage
--               represents.
-- Key technique: Subquery computes days_to_cancel per record
--               using julianday() date arithmetic.
--               Outer query uses CASE day-range buckets (<=35
--               days per box cycle) to label each stage, and
--               SUM … OVER() window function for the % column.
-- ================================================================

SELECT
    CASE
        WHEN days_to_cancel <= 35 THEN '1 - Churned after 1st box'
        WHEN days_to_cancel <= 65 THEN '2 - Churned after 2nd box'
        WHEN days_to_cancel <= 95 THEN '3 - Churned after 3rd box'
        ELSE                           '4 - Long-term churn (4+ boxes)'
    END                                                         AS churn_stage,
    COUNT(*)                                                    AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)         AS pct
FROM (
    SELECT
        CAST(julianday(ca.cancel_date) - julianday(s.start_date) AS INT) AS days_to_cancel
    FROM   cancellation ca
    JOIN   subscription s ON ca.subscription_id = s.subscription_id
)
GROUP  BY churn_stage
ORDER  BY churn_stage;
