WITH source AS (
SELECT
	machineType
	, CASE 
		WHEN machineType = 'Perfuratriz' THEN 'PER'
		WHEN machineType = 'Escavadeira Hidráulica' THEN 'ESH'
		WHEN machineType = 'Caminhão Fora de Estrada' THEN 'CAM'
		WHEN machineType = 'Carregadeira' THEN 'CAR'
		ELSE 'BPR'
	END AS machine_code
	, incidentType AS incident_type
	, severity AS incident_severity
FROM {{ref('stg_incidents')}}
GROUP BY incidentType, machineType, severity
ORDER BY machine_code
)

SELECT
	ROW_NUMBER() OVER (ORDER BY machine_code) AS incident_id
	, machine_code
	, incident_type
	, incident_severity
	, CURRENT_TIMESTAMP AS ingestion_timestamp
FROM source