
SELECT 
    id AS product_id,
    TRIM(name) AS product_name,
    LOWER(category) AS product_category,
    price AS unit_price,
    CASE 
        WHEN price < 50 THEN 'Low Range'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid Range'
        ELSE 'High Range'
    END AS price_segment
FROM {{ source('raw_data', 'products') }}