{{ config(materialized='table', schema='RAW') }}

with order_data as (
    select 
        o.customer_id,
        o.order_date,
        oi.total_price
    from {{ ref('stg_orders') }} o
    join {{ ref('stg_order_items') }} oi on o.order_id = oi.order_id
),

customer_summary as (
    select
        customer_id,
        count(*) as total_orders,
        sum(total_price) as total_spent,
        avg(total_price) as avg_spent,
        max(order_date) as last_purchase_date
    from order_data
    group by 1
)

select 
    customer_id,
    total_orders,
    total_spent,
    avg_spent,
    case when last_purchase_date < '2024-02-01' then 1 else 0 end as target_churn
from customer_summary