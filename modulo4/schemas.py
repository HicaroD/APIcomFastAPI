from pydantic import BaseModel


class EstudanteSchema(BaseModel):
    matricula: int
    nome: str
    idade: int

    class Config:
        orm_mode = True

class EstudanteUpdate(BaseModel):
    matricula: int | None
    nome: str | None
    idade: int | None