SELECT
    *
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM {{source('astarte', 'maintenances')}}