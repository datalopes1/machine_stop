SELECT
    incident_id
    , machine_code
    , incident_type
    , incident_severity
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM {{ref('dim_incidents')}}