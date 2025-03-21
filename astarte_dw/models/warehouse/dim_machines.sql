WITH source AS (
    SELECT 
        machineId::INT AS machine_id
        , purchaseDate AS purchase_date
        , machineType AS machine_type
        , CASE
            WHEN machineType = 'Perfuratriz' THEN 'PER'
            WHEN machineType = 'Escavadeira Hidráulica' THEN 'ESH'
            WHEN machineType = 'Caminhão Fora de Estrada' THEN 'CAM'
            WHEN machineType = 'Carregadeira' THEN 'CAR'
            ELSE 'BPR'		
        END AS machine_type_id
        , operationalCost AS operational_cost
    FROM {{ref('stg_machines')}}
    WHERE machineId IS NOT NULL
)

SELECT
    *
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM source

