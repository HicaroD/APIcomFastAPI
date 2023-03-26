from sqlalchemy import Column, Integer, String
from database import Base


# Essa classe "Estudante" representa uma tabela em nosso banco de dados.
# Para fazer com que ela represente uma classe no banco de dados, nós herdamos
# de "Base", como explicado no arquivo "database.py"
class Estudante(Base):
    # Essa variável é importante porque precisamos mapear essa classe
    # para o nome verdadeiro da tabela lá no banco de dados, nesse caso
    # o nome da tabela é "estudantes"
    __tablename__ = "estudantes"

    # Aqui iremos dizer quais os nomes das colunas da tabela lá no
    # banco de dados. Os nomes das variáveis abaixo devem condizer com
    # o nome dado as colunas lá no banco de dados, dessa forma, preste atenção nisso.
    matricula = Column(Integer, primary_key=True, index=True, nullable=False)
    nome = Column(String, index=True, nullable=False)
    idade = Column(Integer, index=True, nullable=False)
