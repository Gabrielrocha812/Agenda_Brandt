import csv
import psycopg2 as pg

# Nome do arquivo CSV existente
csv_file = 'test_hr.csv'

# Conexão com o banco de dados PostgreSQL para truncar a tabela (se necessário)
pg_conn = pg.connect("postgresql://postgres:K7TI0ctUHrGMXbE@akasha.eco.br:5432/agenda_brandt")
pg_cursor = pg_conn.cursor()

# Truncate the table to remove existing data (optional, if needed)
# pg_cursor.execute("TRUNCATE TABLE hora_real_usu")
# pg_conn.commit()

# Determinar os campos a serem exportados (incluindo a coluna `id`)
fields = ['id'] + [
    'cod_projeto', 'cod_usuario', 'nom_usuario', 'cod_projeto_alfa', 'dth_inicio',
    'dth_prevista', 'nom_contato', 'flg_status_projeto_raiz', 'total_horas_alocadas',
    'nom_projeto', 'pai'
]

cmd = f"COPY hora_real_usu({','.join(fields)}) FROM STDIN WITH CSV HEADER DELIMITER ','"
with open("test_hr.csv", "r", encoding='utf-8') as f:
    pg_cursor.copy_expert(cmd, f)
pg_conn.commit()

# Fechando as conexões
pg_cursor.close()
pg_conn.close()
