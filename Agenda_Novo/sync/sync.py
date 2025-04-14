import os
import csv
import pymysql
import psycopg2 as pg
import sqlalchemy as sa
from datetime import datetime
import msal
import requests

# Configurações do MSAL e API Graph
CLIENT_ID = 'a4d5bd55-41d1-466d-b206-fcc7f10a6dde'
CLIENT_SECRET = 'A7P8Q~nMlchtpNVYmimrZ5-d_q.AosMM6n3rQbnR'
TENANT_ID = 'bb9448e1-a7ac-4440-b3f2-31de071ace07'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPES = ['https://graph.microsoft.com/.default']
EMAIL_TO = ['gabriel.rocha@brandt.com.br', 'davi.santos@brandt.com.br']  # Destinatário do email
SENDER_EMAIL = 'gabriel.rocha@brandt.com.br'  # Seu email para enviar

# Função para autenticar e obter o token de acesso
def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception('Não foi possível obter o token de acesso.')

# Função para enviar e-mail usando a API Microsoft Graph
def send_email(subject, body):
    access_token = get_access_token()
    endpoint = f'https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    
    # Criar a lista de destinatários
    to_recipients = [{'emailAddress': {'address': recipient}} for recipient in EMAIL_TO]
    
    email_message = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'Text',
                'content': body
            },
            'toRecipients': to_recipients
        }
    }
    response = requests.post(endpoint, headers=headers, json=email_message)
    if response.status_code == 202:
        print('Email enviado com sucesso.')
    else:
        print(f'Falha ao enviar o e-mail: {response.status_code} {response.text}')

# O restante do seu código permanece o mesmo...

def is_valid_date(date_str):
    try:
        if date_str == '0000-00-00' or date_str.startswith('0000'):
            return False
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

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
mysql_engine = sa.create_engine("mysql+pymysql://brandt:qeq94827GYGIUH@desenv.netproject.com.br:3306/netproject_brandt_readonly")
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

# Variáveis para armazenar linhas problemáticas
error_rows = []
log_lines = []

# Adicionar o campo id incremental aos dados
valid_rows = []
for i, row in enumerate(result):
    row['id'] = max_id + i + 1
    try:
        # Verificar se as datas são inválidas
        if not is_valid_date(row['dth_inicio']) or not is_valid_date(row['dth_prevista']):
            raise ValueError(f"Data inválida encontrada: dth_inicio={row['dth_inicio']}, dth_prevista={row['dth_prevista']}")
        # Se estiver tudo certo, adiciona à lista de linhas válidas
        valid_rows.append(row)
    except Exception as e:
        # Se houver erro, registra no log
        log_lines.append(f"Erro na linha {i}: {str(e)}")
        error_rows.append(row)

# Gravar apenas linhas válidas no CSV
if valid_rows:
    with open('test_hr.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(valid_rows)

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

# Se houver problemas, envia o log por e-mail
if log_lines:
    log_content = "\n".join(log_lines)
    send_email("Problemas ao Inserir Dados no PostgreSQL", log_content)
