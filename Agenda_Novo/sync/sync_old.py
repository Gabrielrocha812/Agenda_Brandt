import os
import csv
import pymysql
import psycopg2 as pg
import sqlalchemy as sa
from sqlalchemy import create_engine

# Deletar o arquivo CSV antigo, se existir
csv_file = 'test_hr.csv'
if os.path.exists(csv_file):
    os.remove(csv_file)

# Conexão com o banco de dados PostgreSQL para truncar a tabela
pg_conn = pg.connect("postgresql://postgres:K7TI0ctUHrGMXbE@akasha.eco.br:5432/agenda_brandt")
pg_cursor = pg_conn.cursor()
pg_cursor.execute("TRUNCATE TABLE hora_real_usu")
pg_conn.commit()

# Criando a conexão com o banco de dados MySQL
mysql_engine = sa.create_engine("mysql+pymysql://brandt:qeq94827GYGIUH@netproject-readonly.cihqshkrwado.sa-east-1.rds.amazonaws.com:3306/netproject_brandt_readonly")
mysql_connection = mysql_engine.raw_connection()
mysql_cursor = mysql_connection.cursor(pymysql.cursors.DictCursor)

# Query para selecionar os dados do banco de dados MySQL
qry = """
SELECT 
    p.cod_projeto,
    u.cod_usuario,
    u.nom_usuario,
    pr.cod_projeto_alfa,
    DATE_FORMAT(p.dth_inicio, '%Y-%m-%d') AS dth_inicio,
    DATE_FORMAT(p.dth_prevista, '%Y-%m-%d') AS dth_prevista,
    c.nom_contato,
    CASE 
        WHEN p.flg_status IN ('1', '2', '3') THEN p.flg_status
        ELSE pr.flg_status_projeto_raiz
    END AS flg_status_projeto_raiz,  
    SUM(dra.num_horas_aloc) AS total_horas_alocadas,
    p.nom_projeto,
    p2.nom_projeto AS pai
FROM 
    projeto p
JOIN 
    DWDT_RECURSO_ALOCACAO dra 
    ON p.cod_projeto = dra.cod_projeto
JOIN 
    usuario u 
    ON dra.cod_usuario = u.cod_usuario
JOIN 
    projeto_raiz pr 
    ON dra.cod_projeto_raiz = pr.cod_projeto
JOIN 
    contato c 
    ON u.cod_subgerencia = c.cod_contato
JOIN 
    projeto p2 
    ON p.cod_projeto_pai = p2.cod_projeto  
WHERE 
    u.flg_ativo = '1'  
    AND pr.flg_status_projeto_raiz NOT IN (40, 90, 100) 
    AND p.flg_status IN ('1', '2', '3') 
GROUP BY 
    p.cod_projeto, 
    u.cod_usuario, 
    u.nom_usuario, 
    pr.cod_projeto_alfa, 
    DATE_FORMAT(p.dth_inicio, '%Y-%m-%d'),
    DATE_FORMAT(p.dth_prevista, '%Y-%m-%d'),
    c.nom_contato, 
    pr.flg_status_projeto_raiz,
    p.nom_projeto,
    p2.nom_projeto  
LIMIT 
    40000;
"""

mysql_cursor.execute(qry)
result = mysql_cursor.fetchall()

# Obter o valor máximo de id da tabela truncada (vai ser sempre 0)
pg_cursor.execute("SELECT COALESCE(MAX(id), 0) FROM hora_real_usu")
max_id = pg_cursor.fetchone()[0]

# Determinar os campos a serem exportados (incluindo a coluna id)
fields = ['id'] + [
    'cod_projeto', 'cod_usuario', 'nom_usuario', 'cod_projeto_alfa', 'dth_inicio',
    'dth_prevista', 'nom_contato', 'flg_status_projeto_raiz', 'total_horas_alocadas',
    'nom_projeto', 'pai'
]

# Adicionar o campo id incremental aos dados
for i, row in enumerate(result):
    row['id'] = max_id + i + 1
    if row['dth_inicio'] == '0000-00-00':
        row['dth_inicio'] = '01-01-2025'
    if row['dth_prevista'] == '0000-00-00':
        row['dth_prevista'] = '01-01-2025'

with open('test_hr.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(result)

# Comando COPY para inserir os dados do CSV no PostgreSQL, ignorando o cabeçalho
cmd = f"COPY hora_real_usu({','.join(fields)}) FROM STDIN WITH CSV HEADER DELIMITER ','"
with open("test_hr.csv", "r", encoding='utf-8') as f:
    pg_cursor.copy_expert(cmd, f)
pg_conn.commit()

# Fechando as conexões
mysql_cursor.close()
mysql_connection.close()
pg_cursor.close()
pg_conn.close()
