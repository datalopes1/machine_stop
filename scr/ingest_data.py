import psycopg2
import csv

# Conecta ao banco de dados
conn = psycopg2.connect(
    host = "",
    database = "",
    user = "",
    password = ""
)

# Cria um cursor
cur = conn.cursor()

# Faz a ingestão dos dados da tabela machine
with open('data/machine.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO machine (machineId, machineType, dataFabricacao, operationalCost) VALUES (%s, %s, %s, %s)",
            row     
        )

# Faz a ingestão dos dados da tabela operators
with open('data/operators.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f) 
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO operators (operatorId, machineId, name, workShift) VALUES (%s, %s, %s, %s)",
            row
        )

# Faz a ingestão dos dados da tabela incidents
with open('data/incidents.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO incidents (incidentId, machineId, machineType, incidentType, incidentDate, severity) VALUES (%s, %s, %s, %s, %s, %s)",
            row
        )

# Faz a ingestão dos dados da tabela maintenance
with open('data/maintenance.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO maintenance (maintenanceId, incidentId, machineId, maintenanceDate, maintenanceCost, downtimeHours) VALUES (%s, %s, %s, %s, %s, %s)",
            row
        )

conn.commit()
cur.close()
conn.close()