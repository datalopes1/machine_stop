import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

WORK_SHIFT = [
    'Manhã',
    'Tarde',
    'Noite'
]

OPERATIONAL_COST = {
    'Escavadeira Hidráulica': 630, 
    'Perfuratriz': 420, 
    'Carregadeira': 500, 
    'Britador Primário': 300, 
    'Caminhão Fora de Estrada': 640
}

MAINTENANCE_TYPE = [
    'Preventiva',
    'Preditiva',
    'Corretiva'
]

INCIDENT_COST = {
    'Escavadeira Hidráulica': [
        ('Vazamento de óleo hidráulico', 12000, 18000),
        ('Desgaste dos dentes da caçamba', 2000, 5000),
        ('Falha no sistema de rotação', 25000, 40000),
        ('Quebra do cilindro hidráulico', 50000, 80000),
    ],
    'Perfuratriz': [
        ('Desgaste da broca', 8000, 15000),
        ('Falha no compressor de ar', 20000, 35000),
        ('Vazamento de combustível', 10000, 18000),
        ('Quebra do motor de perfuração', 80000, 120000)

    ],
    'Carregadeira': [
        ('Desgaste dos pneus', 15000, 25000),
        ('Falha no sistema hidráulico', 18000, 30000),
        ('Superaquecimento do motor', 25000, 40000),
        ('Danos na caçamba de carga', 50000, 70000)
    ],
    'Britador Primário': [
        ('Bloqueio por material', 5000, 10000),
        ('Desgaste das mandíbulas', 20000, 35000),
        ('Falha no motor elétrico', 40000, 60000),
        ('Rompimento de correias', 15000, 25000)
    ],
    'Caminhão Fora de Estrada': [
        ('Desgaste das pastilhas de freio', 8000, 12000),
        ('Falha no sistema de transmissão', 30000, 50000),
        ('Vazamento de óleo do motor', 15000, 25000),
        ('Quebra do eixo traseiro', 80000, 150000)
    ]
}

INCIDENT_SEVERITY = {
    'Baixa': [1, 4],
    'Média': [4, 24],
    'Alta': [24, 72],
    'Crítica': [72, 168]
}

FILE_PATHS = {
    'machine': 'data/machine.xlsx',
    'operators': 'data/operators.xlsx',
    'incidents': 'data/incidents.xlsx',
    'maintenance': 'data/maintenance.xlsx'
}

def machine_data(n_entries: int, start_date: str, end_date: str) -> pd.DataFrame:
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    data = []

    for _ in range(n_entries):

        machine_type = random.choice(list(OPERATIONAL_COST.keys()))

        data.append({
            'machineId': f"{_ + 1:04}",
            'machineType': machine_type,
            'dataFrabricacao': fake.date_between(start_date=start_date, end_date=end_date),
            'operationalCost': OPERATIONAL_COST[machine_type],
        })
    
    return pd.DataFrame(data)

def operators_data(n_entries: int, machine_df: pd.DataFrame) -> pd.DataFrame:

    data = []

    for _ in range(n_entries):

        machine_id = random.choice(machine_df['machineId'])

        data.append({
            'operatorId': f"{_ + 1:04}",
            'machineId': machine_id,
            'name': fake.name(),
            'workShift': random.choice(WORK_SHIFT)
        })

    return pd.DataFrame(data)

def incident_data(n_entries: int, start_date: str, end_date: str, machine_df: pd.DataFrame) -> pd.DataFrame:

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    data = []

    for _ in range(n_entries):

        machine_id = random.choice(machine_df['machineId'])
        machine_type = machine_df[machine_df['machineId'] == machine_id]['machineType'].values[0]
        incident_type = random.choice(INCIDENT_COST[machine_type])

        data.append({
            'incidentId': f"{_ + 1:04}",
            'machineId': machine_id,
            'machineType': machine_type,
            'incidentType': incident_type[0],
            'incidentDate': fake.date_between(start_date=start_date, end_date=end_date),
            'severity': random.choice(list(INCIDENT_SEVERITY.keys())),
        })

    return pd.DataFrame(data)

def maintenance_data(n_entries: int, incident_data: pd.DataFrame) -> pd.DataFrame:

    data = []

    for _ in range(n_entries):

        incident_id = random.choice(incident_data['incidentId'])
        incident_row = incident_data[incident_data['incidentId'] == incident_id].iloc[0]

        machine_type = incident_row['machineType']
        incident_type = next(
            item for item in INCIDENT_COST[machine_type] if item[0] == incident_row['incidentType']
        )

        data.append({
            'maintenanceId': f"{_ + 1:04}",
            'incidentId': incident_id,
            'machineId': incident_row['machineId'],
            'maintenanceDate': incident_row['incidentDate'],
            'maintenanceCost': round(random.uniform(incident_type[1], incident_type[2]), 2),
            'downtimeHours': random.randint(
                INCIDENT_SEVERITY[incident_row['severity']][0],
                INCIDENT_SEVERITY[incident_row['severity']][1]
            ),
        })

    return pd.DataFrame(data)

if __name__=="__main__":
    """
    Gerar dados fictícios para as máquinas, operadores, incidentes e manutenções
    """
    machine = machine_data(70, '2014-01-01', '2023-12-31')
    operators = operators_data(210, machine)
    incidents = incident_data(750, '2024-01-01', '2024-12-31', machine)
    maitenance = maintenance_data(750, incidents)

    machine.to_excel(FILE_PATHS['machine'], index=False)
    print(f"Dados das máquinas salvos com sucesso em {FILE_PATHS['machine']}")

    operators.to_excel(FILE_PATHS['operators'], index=False)   
    print(f"Dados dos operadores salvos com sucesso em {FILE_PATHS['operators']}")

    incidents.to_excel(FILE_PATHS['incidents'], index=False)
    print(f"Dados dos incidentes salvos com sucesso em {FILE_PATHS['incidents']}")

    maitenance.to_excel(FILE_PATHS['maintenance'], index=False)
    print(f"Dados das manutenções salvos com sucesso em {FILE_PATHS['maintenance']}")