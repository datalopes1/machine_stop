WITH source AS (
    SELECT 
        operatorId::INT AS operator_id
        , machineId AS machine_id
        , operatorName AS operator_name
        , workShift AS work_shift
    FROM {{ref('stg_operators')}}
)

SELECT
    *
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM source

