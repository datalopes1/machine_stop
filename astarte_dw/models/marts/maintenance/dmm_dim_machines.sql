SELECT 
    machine_id
    , machine_type
    , machine_code
    , purchase_date
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM {{ref('dim_machines')}}