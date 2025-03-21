SELECT
    maintenance_id
    , machine_id
    , incident_id
    , maintenance_date
    , downtime_hours
    , maintenance_cost
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM {{ref('fact_maintenances')}}