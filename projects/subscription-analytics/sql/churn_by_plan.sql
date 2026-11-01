-- ================================================================
-- Q4H  Churn Rate & Average Subscription Tenure by Plan
-- ----------------------------------------------------------------
-- What it does : For each subscription plan, shows the total
--               subscriber count, number cancelled vs active,
--               churn rate percentage, average tenure of
--               cancelled subscribers, and average tenure of
--               currently active subscribers.
--               Answers: which plan has the highest churn rate,
--               and do cancelled subscribers stay longer in
--               certain plans before leaving?
-- Key technique: Conditional SUM (SUM + CASE) counts cancelled
--               and active subscribers in one pass. Conditional
--               AVG computes separate tenure averages for each
--               status group without a self-join. LEFT JOIN on
--               cancellation retrieves the cancel_date only for
--               cancelled subscriptions.
-- ================================================================

SELECT
    sp.subscription_plan_name                                        AS plan,
    COUNT(DISTINCT s.subscription_id)                                AS total_subscribers,
    SUM(CASE WHEN s.status = 'Cancelled' THEN 1 ELSE 0 END)         AS cancelled,
    SUM(CASE WHEN s.status = 'Active'    THEN 1 ELSE 0 END)         AS active,
    ROUND(SUM(CASE WHEN s.status = 'Cancelled' THEN 1 ELSE 0 END)
          * 100.0 / NULLIF(COUNT(DISTINCT s.subscription_id), 0), 1) AS churn_rate_pct,
    ROUND(AVG(
        CASE WHEN s.status = 'Cancelled'
             THEN CAST(julianday(ca.cancel_date)
                     - julianday(s.start_date) AS REAL) / 30
        END
    ), 1)                                                            AS avg_tenure_cancelled_months,
    ROUND(AVG(
        CASE WHEN s.status = 'Active'
             THEN CAST(julianday('2026-02-28')
                     - julianday(s.start_date) AS REAL) / 30
        END
    ), 1)                                                            AS avg_tenure_active_months
FROM   subscription s
JOIN   subscription_plan sp ON s.subscription_plan_id = sp.subscription_plan_id
LEFT JOIN cancellation ca   ON s.subscription_id      = ca.subscription_id
GROUP  BY sp.subscription_plan_name
ORDER  BY churn_rate_pct DESC;
