from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_database():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()


app = FastAPI()


@app.get("/estudantes", response_model=list[schemas.BaseEstudante])
def get_all_students(database: Session = Depends(get_database)):
    users = database.query(models.Estudante).all()
    return users


@app.get("/estudante/{matricula}/", response_model=schemas.BaseEstudante)
def get_student_by_matricula(matricula: int, database: Session = Depends(get_database)):
    user = (
        database.query(models.Estudante)
        .filter(models.Estudante.matricula == matricula)
        .first()
    )
    return user


@app.post("/estudante/create/", response_model=schemas.BaseEstudante, status_code=201)
def create_student(
    estudante: schemas.BaseEstudante,
    database: Session = Depends(get_database),
):
    novo_estudante = models.Estudante(**estudante.dict())

    # O código abaixo é equivalente a linha de cima.
    # Perceba que os campos são de estudante do model do banco de dados e do
    # schema da API, então é melhor usar a linha de cima.
    # Se fossem campos com nomes diferentes, então deveríamos usar o código comentado abaixo

    # novo_estudante = models.Estudante(
    #     matricula=estudante.matricula,
    #     nome=estudante.nome,
    #     idade=estudante.idade,
    # )

    database.add(novo_estudante)
    database.commit()
    database.refresh(novo_estudante)
    return novo_estudante


@app.delete("/estudante/delete/{matricula}")
def delete_student(matricula: int, database: Session = Depends(get_database)):
    database.query(models.Estudante).filter(
        models.Estudante.matricula == matricula
    ).delete()
    database.commit()
    return {
        "detail": f"Estudante deletado com matricula {matricula} foi removido com sucesso"
    }


@app.patch("/estudante/update/{matricula}")
def update_student(
    matricula: int,
    estudante: schemas.EstudanteUpdate,
    database: Session = Depends(get_database),
):
    student_from_db = database.query(models.Estudante).filter(
        models.Estudante.matricula == matricula
    ).first()

    updated_student = estudante.dict(exclude_unset=True)
    for key, value in updated_student.items():
        setattr(student_from_db, key, value)
    database.commit()
    database.refresh(student_from_db)
    return {"detail": "Estudante atualizado com sucesso"}
