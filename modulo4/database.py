from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Esse é o URL do nosso banco de dados.
SQLITE_URL = "sqlite:///./estudante.db"

# A partir do URL do nosso banco de dados, iremos criar uma engine com o URL
# Pense na engine como a conexão com o banco de dados, por isso que usamos o URL
# do banco de dados para a engine ter acesso
engine = create_engine(
    SQLITE_URL,
    # Atenção: essa opção abaixo é necessária para SQLite, não para os outros banco de dados
    connect_args={
        "check_same_thread": False,
    },
)

# Iremos usar essa variável para criar sessões.
# Nós criamos sessões para interagir com o banco de dados. É uma sessão de acesso, quando
# essa sessão fecha, não podemos mais interagir, só se criarmos outra sessão
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Essa variável será usada nas classes do Python que irão representar tabelas no
# banco de dados. Toda vez que queremos criar uma classe no Python e essa classe
# irá representar uma tabela no banco de dados, então teremos que fazer com que a
# a classe herde de Base, como você verá no arquivo "models.py"
Base = declarative_base()
