from sqlalchemy import Column, Integer, String

from database import Base

class Estudante(Base):
    __tablename__ = "estudantes"

    matricula = Column(Integer, primary_key=True, index=True, nullable=False)
    nome = Column(String, index=True, nullable=False)
    idade = Column(Integer, index=True, nullable=False)