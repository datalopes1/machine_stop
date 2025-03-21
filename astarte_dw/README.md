# 🏭 Astarte Data Warehouse

## Processo de Modelagem dimensional
### 1. Definir o processo de negócio

|Processo de Negócio|Tabela Fato|Tipo de Grão do Fato|Granularidade|machine|operator|incident|date|Prioridade|
|---|---|---|---|---|---|---|---|---|
|Manutenção|fact_maintenance|Transacão|Uma linha por manutenção|x| |x|x|Alta|

### 2. Declarar a granularidade
- **fact_maintenance**: Uma linha por manutenção

### 3. Identificar as dimensões

|Dimensão|Atributos|
|---|---|
|**dim_machines**|`machine_id`, `machine_type_id`, `machine_type`, `purchaseDate`|
|**dim_incidents**|`incident_id`, `machine_type_id`, `incident_type`, `incident_severity`|
|**dim_date**|`date_key`, `full_date`, `year`, `month`, `day`, `quarter`, `day_of_week`, `day_name`, `month_name`, `is_weekend`|

### 4. Identificar os fatos

**fact_maintenance**

|Coluna|Tipo|Descrição|
|---|---|---|
|**maintenance_id**|VARCHAR|Identificador único da manutenção|
|**machine_id**|VARCHAR|Identificador único da máquina|
|**incident_id**|VARCHAR|Identificador único do incidente|
|**maintenance_date**|DATE|Data da manutenção|
|**downtimeHours**|INT|Tempo de parada|
|**maintenanceCost**|FLOAT|Custo de manutenção|