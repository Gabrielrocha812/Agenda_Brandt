

# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Configurações do banco de dados datalake
DATABASE_URL = "postgresql://postgres:K7TI0ctUHrGMXbE@akasha.eco.br:5432/agenda_brandt"

# Criação do engine
engine = create_engine(DATABASE_URL)

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de classes de modelo
Base = declarative_base()

