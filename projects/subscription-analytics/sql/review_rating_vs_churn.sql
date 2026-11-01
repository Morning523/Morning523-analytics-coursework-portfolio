-- ================================================================
-- Q4D  Review Rating vs Subsequent Churn Rate
-- ----------------------------------------------------------------
-- What it does : Groups customers by the rating band of their
--               review (1-2 Negative / 3 Neutral / 4-5 Positive)
--               and calculates what percentage of each group
--               later cancelled their subscription.
--               Answers: do customers who leave negative reviews
--               churn at a higher rate?
-- Key technique: CASE bucketing in a subquery classifies each
--               reviewer's rating into a band. The outer query
--               then joins subscription status to compute the
--               churn rate per band using NULLIF-guarded division.
-- ================================================================

SELECT
    rating_band,
    total_reviewers,
    churned_after_review,
    ROUND(churned_after_review * 100.0
          / NULLIF(total_reviewers, 0), 1)                      AS churn_rate_pct
FROM (
    SELECT
        CASE
            WHEN rv.rating <= 2 THEN '1-2  (Negative)'
            WHEN rv.rating  = 3 THEN '3    (Neutral)'
            ELSE                     '4-5  (Positive)'
        END                                                     AS rating_band,
        COUNT(DISTINCT rv.customer_id)                          AS total_reviewers,
        COUNT(DISTINCT CASE WHEN s.status = 'Cancelled'
                            THEN rv.customer_id END)            AS churned_after_review
    FROM   review rv
    JOIN   subscription s ON rv.customer_id = s.customer_id
    GROUP  BY rating_band
)
ORDER  BY rating_band;
