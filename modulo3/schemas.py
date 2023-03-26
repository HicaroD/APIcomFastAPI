from pydantic import BaseModel


class BaseEstudante(BaseModel):
    matricula: int | None
    nome: str | None
    idade: int | None

    class Config:
        orm_mode = True


class EstudanteUpdate(BaseEstudante):
    matricula: int | None = None
    nome: str | None = None
    idade: int | None = None
