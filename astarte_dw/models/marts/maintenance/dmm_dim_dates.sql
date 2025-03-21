SELECT
    full_date AS data,
    year AS ano,
    month AS mes_num,
    day AS dia,
    quarter AS trimestre,
    day_of_week AS dia_da_semana,
    day_name AS dia_nome,
    month_name AS mes_nome,
    CASE 
        WHEN is_weekend = 'Weekend' THEN 'Sim'
        ELSE 'Não'
    END AS fim_de_semana  
FROM {{ ref('dim_dates') }}  
WHERE full_date BETWEEN
    (SELECT DATE_TRUNC('year', MIN(maintenance_date)) FROM {{ ref('fact_maintenances') }}) 
    AND 
    (SELECT DATE_TRUNC('year', MAX(maintenance_date)) + INTERVAL '1 year - 1 day' FROM {{ ref('fact_maintenances') }})