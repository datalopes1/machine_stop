# ----- IMPORTS -----
import psycopg2
import csv
from tqdm import tqdm

# ----- FUNÇÕES -----
def count_rows(file_path: str) -> int:
    """
    Conta o total de linhas em um arquivo .csv

    Parâmetros:
        file_path: str - Caminho do arquivo .csv

    Retorna:
        int - Número de linhas no arquivo .csv
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        return sum(1 for _ in reader)

def insert_data(cur, file_path, table_name, columns):
    """
    Faz a ingestão de dados no banco de dados postgresql

    Parâmetros:
        cur: psycopg2.cursor - Cursor do banco de dados
        file_path: str - Caminho do arquivo .csv
        table_name: str - Nome da tabela
        columns: List[str] - Lista com os nomes das colunas
    """
    total_rows = count_rows(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in tqdm(reader, total=total_rows, desc=f"Inserindo dados em {table_name}", unit="linha"):
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cur.execute(query, row)

if __name__=="__main__":
    # Conexão com o banco de dados
    conn = psycopg2.connect(
    host = "",
    database = "",
    user = "",
    password = ""
    )
    cur = conn.cursor()

    # Caminho dos arquivos, tabelas e colunas
    tables = [
        {
            'file_path': 'data/machine.csv',
            'table_name': 'machine',
            'columns': ['machineId', 'machineType', 'dataFabricacao', 'operationalCost']
        },
        {
            'file_path': 'data/operators.csv',
            'table_name': 'operators',
            'columns': ['operatorId', 'machineId', 'name', 'workShift']
        },
        {
            'file_path': 'data/incidents.csv',
            'table_name': 'incidents',
            'columns': ['incidentId', 'machineId', 'machineType', 'incidentType', 'incidentDate', 'severity']
        },
        {
            'file_path': 'data/maintenance.csv',
            'table_name': 'maintenance',
            'columns': ['maintenanceId', 'incidentId', 'machineId', 'maintenanceDate', 'maintenanceCost', 'downtimeHours']
        }
    ]

    # Ingestão dos dados
    for table in tables:
        insert_data(cur, table['file_path'], table['table_name'], table['columns'])

    conn.commit()
    print("Dados inseridos com sucesso!")
    cur.close()
    conn.close()    
