WITH source AS (
SELECT
	machineType
	, CASE 
		WHEN machineType = 'Perfuratriz' THEN 'PER'
		WHEN machineType = 'Escavadeira Hidráulica' THEN 'ESH'
		WHEN machineType = 'Caminhão Fora de Estrada' THEN 'CAM'
		WHEN machineType = 'Carregadeira' THEN 'CAR'
		ELSE 'BPR'
	END AS machine_type_id
	, incidentType AS incident_type
	, severity AS incident_severity
FROM {{ref('stg_incidents')}}
GROUP BY incidentType, machineType, severity
ORDER BY machine_type_id
)

SELECT
	ROW_NUMBER() OVER (ORDER BY machine_type_id) AS incident_id
	, machine_type_id
	, incident_type
	, incident_severity
	, CURRENT_TIMESTAMP AS ingestion_timestamp
FROM source