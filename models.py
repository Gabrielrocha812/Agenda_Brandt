from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

#inicio login classe
class LoginData(BaseModel):
    username: str
    password: str

#fim login classe

#dados netproject de cada setor inicio
class hora_real_usuario(Base):
    __tablename__ = 'hora_real_usu'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_usuario %r>'%(self.id)
    
class hora_real_geo(Base):
    __tablename__ = 'hora_real_usuario'

    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_geo.cod_projeto"))  # ForeignKey definida aqui
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))

    def __repr__(self):
        return f'<hora_real_usuario id={self.id}, cod_projeto="{self.cod_projeto}">'
    
class hora_real_arqueologia(Base):
    __tablename__ = 'hora_real_arqueologia'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_arqueologia.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_arqueologia %r>'%(self.id)

class hora_real_biodiversidade(Base):
    __tablename__ = 'hora_real_biodiversidade'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_bio.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_biodiversidade %r>'%(self.id)

class hora_real_espeleologia(Base):
    __tablename__ = 'hora_real_espeleologia'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_esp.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_espeleologia %r>'%(self.id)
    
class hora_real_humanidades(Base):
    __tablename__ = 'hora_real_humanidades'
    
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_hum.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))

    def __repr__(self):
        return f'<hora_real_humanidades id={self.id}>'
  
class hora_real_mfisico(Base):
    __tablename__ = 'hora_real_mfisico'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_mf.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_mfisico %r>'%(self.id)    
    
class hora_real_mmodelagens(Base):
    __tablename__ = 'hora_real_mmodelagens'
    id = Column(Integer, primary_key=True)
    cod_projeto = Column(String(150), ForeignKey("demandas_mod.cod_projeto"))
    pai = Column(String(150))
    total_horas_alocadas = Column(Integer)
    nom_projeto = Column(String(150))
    nom_usuario = Column(String(150))
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    cod_projeto_alfa = Column(String(150))
    cod_usuario = Column(String(150))
    nom_contato = Column(String(150))
    flg_status_projeto_raiz = Column(String(150))
    def _repr_(self):
        return '<hora_real_mmodelagens %r>'%(self.id)    
    
            
#fim

#inicio demandas 

class Demandas_Arqueologia(Base):
    __tablename__ = 'demandas_arqueologia'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150), unique=True)
    
    hora_real_usuario = relationship(
        "hora_real_arqueologia",
        backref="demandas_arqueologia",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_Arqueologia id={self.id}, titulo="{self.titulo}">'
    
class Demandas_Biodiversidade(Base):
    __tablename__ = 'demandas_bio'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    hora_real_usuario = relationship(
        "hora_real_biodiversidade",
        backref="demandas_bio",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_Biodiversidade id={self.id}, titulo="{self.titulo}">'
 
class Demandas_Espeleologia(Base):
    __tablename__ = 'demandas_esp'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    hora_real_usuario = relationship(
        "hora_real_espeleologia",
        backref="demandas_esp",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_Espeleologia id={self.id}, titulo="{self.titulo}">'
       
class Demandas_Geo(Base):
    __tablename__ = 'demandas_geo'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(250))
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String(250))
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150), unique=True)  # Adicione `unique=True` para garantir que seja uma chave única.

    # Relacionamento com hora_real_usuario
    hora_real_usuario = relationship(
        "hora_real_geo",
        backref="demanda_geo",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_Geo id={self.id}, titulo="{self.titulo}">'
       
class Demandas_Humanidades(Base):
    __tablename__ = 'demandas_hum'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    def __repr__(self):
        return f'<Demandas_Humanidades id={self.id}, titulo="{self.titulo}">'

class Demandas_MeioFisico(Base):
    __tablename__ = 'demandas_mf'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    hora_real_usuario = relationship(
        "hora_real_mfisico",
        backref="demandas_mf",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_MeioFisico id={self.id}, titulo="{self.titulo}">'
    
class Demandas_Modelagens(Base):
    __tablename__ = 'demandas_mod'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    hora_real_usuario = relationship(
        "hora_real_mmodelagens",
        backref="demandas_mod",  # Relacionamento reverso
        lazy="joined"
    )

    def __repr__(self):
        return f'<Demandas_Modelagens id={self.id}, titulo="{self.titulo}">'
        
class Demandas(Base):
    __tablename__ = 'demandas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))


    def __repr__(self):
        return '<Demandas %r>' % (self.id)

class Demandas_Gestao(Base):
    __tablename__ = 'demandas_gestao'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    hub = Column(String(150))
    responsavel = Column(String(150))
    projeto = Column(String(150))
    atividade = Column(String)
    dth_inicio = Column(Date)
    dth_fim = Column(Date)
    horas_np = Column(String(150))
    n_hora_hub = Column(String(150))
    status = Column(String(150))
    dtinicionp = Column(Date)
    dtfimnp = Column(Date)
    cod_projeto = Column(String(150))

    hora_real_usuario = relationship(
        "Gestao",
        backref="Demandas_Gestao",
        lazy="joined"
    )

#fim demandas 

#inicio aquisição
class AquisicaoArq(Base):
    __tablename__ = 'aquisicao_arq'

    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoArq(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoBio(Base):
    __tablename__ = 'aquisicao_bio'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoBio(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoEsp(Base):
    __tablename__ = 'aquisicao_esp'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoEsp(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoGeo(Base):
    __tablename__ = 'aquisicao_geo'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoGeo(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoHum(Base):
    __tablename__ = 'aquisicao_hum'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoHum(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoMF(Base):
    __tablename__ = 'aquisicao_mf'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoMF(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )

class AquisicaoMod(Base):
    __tablename__ = 'aquisicao_mod'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto_alfa = Column(String, nullable=False)
    pai_aquisicao = Column(Integer, nullable=True)
    nom_projeto = Column(String, nullable=False)
    txt_comentario = Column(String, nullable=True)
    dth_inicio_real = Column(DateTime, nullable=True)
    dth_fim_real = Column(DateTime, nullable=True)
    dsc_aquisicao = Column(String, nullable=True)
    txt_objeto = Column(String, nullable=True)
    dsc_aquisicao_tipo = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<AquisicaoMod(cod_projeto_alfa={self.cod_projeto_alfa}, "
            f"nom_projeto='{self.nom_projeto}', dth_inicio_real={self.dth_inicio_real}, "
            f"dth_fim_real={self.dth_fim_real})>"
        )
    
#fim aquisição

#inicio gestao

class Gestao(Base):
    __tablename__ = 'hora_gestao'
    id= Column(Integer, primary_key=True, nullable=False)
    cod_projeto = Column(String, ForeignKey("demandas_gestao.cod_projeto"))
    cod_usuario = Column(String)
    nom_usuario = Column(String)
    cod_projeto_alfa = Column(String)
    dth_inicio = Column(Date)
    dth_prevista = Column(Date)
    nom_contato = Column(String)
    flg_status_projeto_raiz = Column(String)
    total_horas_alocadas = Column(Float)
    nom_projeto = Column(String)
    pai = Column(String)

#fim gestao

