-- ================================================================
-- Q1B  Average Customer Lifetime Value (CLV) by Subscription Plan
-- ----------------------------------------------------------------
-- What it does : Calculates average, min, and max CLV for each
--               plan based on completed payments only.
-- Key technique: Subquery pre-aggregates total revenue per
--               customer; LEFT JOIN ensures customers with zero
--               completed orders are still included (NULL CLV)
--               rather than being silently excluded.
-- ================================================================

SELECT
    sp.subscription_plan_name        AS plan,
    COUNT(DISTINCT c.customer_id)    AS customers,
    ROUND(AVG(rev.total_revenue), 2) AS avg_clv,
    ROUND(MIN(rev.total_revenue), 2) AS min_clv,
    ROUND(MAX(rev.total_revenue), 2) AS max_clv
FROM   customer c
JOIN   subscription s
           ON c.customer_id = s.customer_id
JOIN   subscription_plan sp
           ON s.subscription_plan_id = sp.subscription_plan_id
LEFT JOIN (
    SELECT   o.customer_id,
             SUM(p.amount) AS total_revenue
    FROM     "order" o
    JOIN     payment p ON o.order_id = p.order_id
    WHERE    p.status = 'Completed'
    GROUP BY o.customer_id
) rev ON c.customer_id = rev.customer_id
GROUP  BY sp.subscription_plan_name
ORDER  BY avg_clv DESC;
