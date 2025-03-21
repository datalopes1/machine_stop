SELECT 
	m.maintenanceid AS maintenance_id
	, m.machineid AS machine_id
	, di.incident_id
	, m.maintenancedate AS maintenance_date
	, m.downtime AS downtime_hours
	, m.maintenancecost AS maintenance_cost
    , CURRENT_TIMESTAMP AS ingestion_timestamp
FROM {{ref('stg_incidents')}} i
LEFT JOIN {{ref('stg_maintenances')}} m
	ON i.incidentId = m.maintenanceId
LEFT JOIN {{ref('dim_incidents')}} di 
	ON i.incidentType = di.incident_type