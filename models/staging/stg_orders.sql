SELECT 
id AS order_id, 
customer_id, 
order_date, 
extract(dayofweek from order_date) as day_of_week, 
extract(month from order_date) as order_month,
status AS order_status
FROM {{ source('raw_data', 'orders') }}
