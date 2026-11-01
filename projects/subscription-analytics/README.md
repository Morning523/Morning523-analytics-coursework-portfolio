# Subscription Analytics

## Business question

In a simulated coffee-subscription case, how do plan, tenure, customer reviews, and purchase patterns relate to customer retention and value? This is a case study built on synthetic data, not a real-company performance assessment.

## Analysis flow

The SQL samples move from customer and revenue measures to retention signals:

- [`churn_by_delivery_stage.sql`](sql/churn_by_delivery_stage.sql) groups cancellations by subscription stage.
- [`churn_by_plan.sql`](sql/churn_by_plan.sql) compares churn rates and tenure across plans.
- [`review_rating_vs_churn.sql`](sql/review_rating_vs_churn.sql) compares subsequent churn across review-rating bands.
- [`customer_lifetime_value_by_plan.sql`](sql/customer_lifetime_value_by_plan.sql) aggregates completed payment value by plan.
- [`synthetic_coffee_sql_analytics.ipynb`](notebooks/synthetic_coffee_sql_analytics.ipynb) demonstrates a wider end-to-end synthetic database and SQL workflow.

The queries demonstrate joins, conditional aggregation, date arithmetic, subqueries, window functions, and null-safe calculations. Tableau visualisations built from SQL outputs are presented separately on my portfolio site.

## Data and contribution

The case uses simulated course data; no customer dataset or database is included. This is team coursework. I participated substantially in the analysis and coding, but the repository does not claim that every query or notebook cell is individually authored.
