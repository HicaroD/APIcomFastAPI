from pydantic import BaseModel


# Importante ressaltar que schema estará relacionado ao modelo do FastAPI
# Já model está relacionado ao model do SQLAlchemy

# Aqui está um model de FastAPI que iremos passar no body da request da API
# Temos essas fields, como int | None, porque naquela field podemos ter um int ou None
class BaseEstudante(BaseModel):
    matricula: int
    nome: str
    idade: int

    class Config:
        orm_mode = True

class EstudanteUpdate(BaseModel):
    matricula: int | None
    nome: str | None
    idade: int | None