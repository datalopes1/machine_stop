import pandas as pd
import numpy as np
import random
from faker import Faker
from tqdm import tqdm

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

# ----- CONSTANTES -----
MACHINES = {
    'Escavadeira Hidráulica': 630.0, 
    'Caminhão Fora de Estrada': 640.0, 
    'Perfuratriz': 420.0, 
    'Carregadeira': 500.0, 
    'Britador Primário': 300.0,
}

INCIDENTS = {
    'Escavadeira Hidráulica': [
        ('Vazamento de óleo hidráulico', "Média", 12000, 18000),
        ('Desgaste dos dentes da caçamba', "Baixa", 2000, 5000),
        ('Falha no sistema de rotação', "Alta", 25000, 40000),
        ('Quebra do cilindro hidráulico', "Crítica", 50000, 80000),
    ],
    'Perfuratriz': [
        ('Desgaste da broca', "Baixa",8000, 15000),
        ('Falha no compressor de ar', "Alta",20000, 35000),
        ('Vazamento de combustível', "Média",10000, 18000),
        ('Quebra do motor de perfuração', "Crítica", 80000, 120000)

    ],
    'Carregadeira': [
        ('Desgaste dos pneus', "Baixa", 15000, 25000),
        ('Falha no sistema hidráulico', "Média", 18000, 30000),
        ('Superaquecimento do motor', "Alta", 25000, 40000),
        ('Danos na caçamba de carga', "Crítica", 50000, 70000)
    ],
    'Britador Primário': [
        ('Bloqueio por material', "Média", 5000, 10000),
        ('Desgaste das mandíbulas', "Baixa", 20000, 35000),
        ('Falha no motor elétrico', "Alta", 40000, 60000),
        ('Rompimento de correias', "Crítica", 15000, 25000)
    ],
    'Caminhão Fora de Estrada': [
        ('Desgaste das pastilhas de freio', "Baixa", 8000, 12000),
        ('Falha no sistema de transmissão', "Alta", 30000, 50000),
        ('Vazamento de óleo do motor', "Média", 15000, 25000),
        ('Quebra do eixo traseiro', "Crítica", 80000, 150000)
    ]
}

OPERATORS_PER_MACHINE = {
    'Escavadeira Hidráulica': 3,
    'Caminhão Fora de Estrada': 2,
    'Perfuratriz': 2,
    'Carregadeira': 1,
    'Britador Primário': 1,
}

DOWNTIME = {
    'Baixa': [1, 4],
    'Média': [4, 24],
    'Alta': [24, 72],
    'Crítica': [72, 168]
}

FILE_PATHS = {
    'machine': 'data/raw/machines.csv',
    'operators': 'data/raw/operators.csv',
    'incidents': 'data/raw/incidents.csv',
    'maintenances': 'data/raw/maintenances.csv'
}

# ----- FUNÇÕES -----
def generate_machine_data(n_entries: int, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Gera os dados de máquinas

    Parâmetros:
        n_entries: int - Quantidade de registros
        start_date: str - Data inicial
        end_date: str - Data final

    Retorna:
        pd.DataFrame - DataFrame com os dados das máquinas
        - machineId: str - Identificador único da máquina
        - machineType: str - Tipo da máquina
        - purchaseDate: str - Data de compra
        - operationalCost: float - Custo operacional por hora trabalhada
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data = []
    
    for idx in tqdm(range(n_entries), desc="Gerando dados das máquinas", unit=" linhas"):
        machine_type = np.random.choice(list(MACHINES.keys()), p=[0.35, 0.25, 0.20, 0.15, 0.05])

        data.append({
            'machineId': f"{idx + 1:03}",
            'machineType': machine_type,
            'purchaseDate': fake.date_between(start_date=start_date, end_date=end_date),
            'operationalCost': MACHINES[machine_type],
        })
    
    return pd.DataFrame(data)

def generate_operator_data(machine_data: pd.DataFrame) -> pd.DataFrame:
    """
    Gera dados dos operadores

    Parâmetros:
        machine_data: pd.DataFrame - DataFrame com os dados das máquinas

    Retorna:
        pd.DataFrame - DataFrame com os dados dos operadores
        - operatorId: str - Identificador único do operador
        - machineId: str - Identificador único da máquina
        - operatorName: str - Nome do operador
        - workShift: str - Turno de trabalho
    """    
    data = []
    operator_id = 1

    for _, row in tqdm(machine_data.iterrows(), total=len(machine_data), desc="Gerando dados dos operadores", unit=" linhas"):
        machine_id = row['machineId']
        machine_type = row['machineType']
        num_operators = OPERATORS_PER_MACHINE[machine_type]

        for _ in range(num_operators):
            data.append({
                'operatorId': f"{operator_id:03}",
                'machineId': machine_id,
                'operatorName': fake.name(),
                'workShift': np.random.choice(['Manhã', 'Tarde', 'Noite'])
            })
            operator_id += 1
    
    return pd.DataFrame(data)

def generate_incident_data(n_entries: int, start_date: str, end_date: str, machine_data: pd.DataFrame) -> pd.DataFrame:
    """
    Gera dados dos incidentes

    Parâmetros:
        n_entries: int - Quantidade de registros
        start_date: str - Data inicial
        end_date: str - Data final
        machine_data: pd.DataFrame - DataFrame com os dados das máquinas
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data = []

    for idx in tqdm(range(n_entries), desc="Gerando dados dos incidentes", unit=" linhas"):
        machine_id = random.choice(machine_data['machineId'])
        machine_row = machine_data[machine_data['machineId'] == machine_id].iloc[0]

        machine_type = machine_row['machineType']
        purchase_date = pd.to_datetime(machine_row['purchaseDate'])

        incident_type, severity, _, _ = random.choice(INCIDENTS[machine_type])
        

        data.append({
            'incidentId': f"{idx + 1:03}",
            'machineId': machine_row['machineId'],
            'machineType': machine_type,
            'incidentType': incident_type,
            'incidentDate': fake.date_between(start_date=purchase_date, end_date=end_date),
            'severity': severity,
        })

    return pd.DataFrame(data)

def generate_maintenance_data(incident_data: pd.DataFrame) -> pd.DataFrame:
    """
    Gera dados das manutenções

    Parâmetros:
        incident_data: pd.DataFrame - DataFrame com os dados dos incidents

    Retorna:
        pd.DataFrame - DataFrame com os dados das manutenções
        - maintenanceId: str - Identificador único da manutenção
        - machineId: str - Identificador único da máquina
        - maintenanceDate: str - Data da manutenção
        - maintenanceCost: float - Custo da manutenção
        - severity: str - Severidade do incidente
        - downtime: int - Tempo de parada da máquina
    """
    data = []
    
    for idx, row in tqdm(incident_data.iterrows(), total=len(incident_data), desc="Gerando dados das manutenções", unit=" linhas"):
        _, _, min_cost, max_cost = INCIDENTS[row['machineType']][0]
        
        data.append({
            'maintenanceId': f"{idx + 1:03}",
            'machineId': row['machineId'],
            'maintenanceDate': row['incidentDate'] + pd.Timedelta(days=1),
            'maintenanceCost': round(np.random.uniform(min_cost, max_cost), 2),
            'severity': row['severity'],
            'downtime': np.random.randint(DOWNTIME[row['severity']][0], DOWNTIME[row['severity']][1])
        })
    
    return pd.DataFrame(data)

# ----- MAIN -----
if __name__=="__main__":
    # Constantes de número de registros
    N_MACHINES = 150
    N_INCIDENTS = N_MACHINES * 12

    # Geração dos dados 
    machine_df = generate_machine_data(N_MACHINES, '2015-01-01', '2024-12-31')
    operator_df = generate_operator_data(machine_df)
    incident_df = generate_incident_data(N_INCIDENTS, '2015-01-01', '2024-12-31', machine_df)
    maintenance_df = generate_maintenance_data(incident_df)

    # Salvar dados
    machine_df.to_csv(f"{FILE_PATHS['machine']}", index=False)
    operator_df.to_csv(f"{FILE_PATHS['operators']}", index=False)
    incident_df.to_csv(f"{FILE_PATHS['incidents']}", index=False)
    maintenance_df.to_csv(f"{FILE_PATHS['maintenances']}", index=False)

    # Validações
    print(f"\nMáquinas: {len(machine_df)}")
    print(f"Incidentes: {len(incident_df)}")
    print(f"Incidentes por máquina: {len(incident_df)/len(machine_df):.1f}")