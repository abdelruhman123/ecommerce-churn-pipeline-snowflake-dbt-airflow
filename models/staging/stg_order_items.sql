SELECT 
    id AS item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    (quantity * unit_price) AS total_price,
    RATIO_TO_REPORT(total_price) OVER (PARTITION BY order_id) AS item_order_weight
FROM {{ source('raw_data', 'order_items') }}