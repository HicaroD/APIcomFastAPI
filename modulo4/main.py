from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_database_session():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()


app = FastAPI()


@app.get("/estudantes", response_model=list[schemas.EstudanteSchema])
def get_all_students(database: Session = Depends(get_database_session)):
    students = database.query(models.Estudante).all()
    return students


@app.get("/estudante/{matricula}", response_model=schemas.EstudanteSchema)
def get_student_by_matricula(
    matricula: int, database: Session = Depends(get_database_session)
):
    student = (
        database.query(models.Estudante)
        .filter(models.Estudante.matricula == matricula)
        .first()
    )

    if not student: # if student is None
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    return student


@app.post("/estudante/create", response_model=schemas.EstudanteSchema, status_code=201)
def create_student(
    estudante: schemas.EstudanteSchema,
    database: Session = Depends(get_database_session),
):
    student = (
        database.query(models.Estudante)
        .filter(models.Estudante.matricula == estudante.matricula)
        .first()
    )

    if student: # if student is not None
        raise HTTPException(status_code=400, detail="Matrícula já cadastrada no sistema")

    novo_estudante = models.Estudante(
        matricula=estudante.matricula,
        nome=estudante.nome,
        idade=estudante.idade,
    )
    database.add(novo_estudante)
    database.commit()
    database.refresh(novo_estudante)
    return novo_estudante


@app.delete("/estudante/delete/{matricula}")
def delete_student(matricula: int, database: Session = Depends(get_database_session)):
    student = (
        database.query(models.Estudante)
        .filter(models.Estudante.matricula == matricula)
        .first()
    )

    if not student: # if student is None
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    database.query(models.Estudante).filter(
        models.Estudante.matricula == matricula
    ).delete()
    database.commit()
    return {"detail": "Estudante removido com sucesso"}


@app.patch("/estudante/update/{matricula}")
def update_student(
    matricula: int,
    estudante: schemas.EstudanteUpdate,
    database: Session = Depends(get_database_session),
):
    student_from_database = (
        database.query(models.Estudante)
        .filter(models.Estudante.matricula == matricula)
        .first()
    )

    if not student_from_database: # if student is None
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    updated_student = estudante.dict(exclude_unset=True)
    for key, value in updated_student.items():
        setattr(student_from_database, key, value)

    database.commit()
    database.refresh(student_from_database)
    return {"detail": "Estudante atualizado com sucesso"}
