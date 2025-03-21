WITH source AS (
  SELECT
    generate_series(
      '2015-01-01'::date,  
      '2035-12-31'::date, 
      '1 day'::interval
    ) AS date
)

SELECT
  TO_CHAR(date, 'YYYYMMDD')::integer AS date_key,  
  date::date AS full_date,
  EXTRACT(YEAR FROM date) AS year,
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(DAY FROM date) AS day,
  EXTRACT(QUARTER FROM date) AS quarter,
  EXTRACT(ISODOW FROM date) AS day_of_week,  
  TO_CHAR(date, 'Day') AS day_name,           
  TO_CHAR(date, 'Month') AS month_name,       
  CASE 
    WHEN EXTRACT(ISODOW FROM date) IN (6, 7) THEN 'Weekend' 
    ELSE 'Weekday' 
  END AS is_weekend
FROM source