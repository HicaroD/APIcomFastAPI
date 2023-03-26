from pydantic import BaseModel


class BaseEstudante(BaseModel):
    matricula: int | None
    nome: str | None
    idade: int | None

    class Config:
        orm_mode = True
