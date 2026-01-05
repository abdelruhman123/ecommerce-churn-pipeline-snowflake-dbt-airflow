WITH customer_info AS (
    SELECT 
        customer_id,
        customer_name,
        email,
        country 
    FROM {{ ref('stg_customers') }}
),

predictions AS (
    SELECT * FROM FINANCE_DB.RAW.CHURN_PREDICTIONS
)

SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.country,
    p.churn_probability,
    p.prediction_date,
    CASE 
        WHEN p.churn_probability > 0.8 THEN 'Critical'
        WHEN p.churn_probability > 0.5 THEN 'At Risk'
        ELSE 'Safe'
    END AS risk_level
FROM customer_info c
JOIN predictions p ON c.customer_id = p.customer_id