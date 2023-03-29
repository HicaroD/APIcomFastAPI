from fastapi import Depends, FastAPI, HTTPException
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
    if not user:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    return user


@app.post("/estudante/create/", response_model=schemas.BaseEstudante, status_code=201)
def create_student(
    estudante: schemas.BaseEstudante,
    database: Session = Depends(get_database),
):
    # Aqui eu fiz a checagem se o estudante existia através da matrícula, caso sim
    # então eu irei retornar um erro dizendo que o estudante já existe com um status code
    # apropriado
    estudante_existe = (
        database.query(models.Estudante)
        .filter(
            models.Estudante.matricula == estudante.matricula,
        )
        .first()
    )
    if estudante_existe:
        raise HTTPException(status_code=404, detail="Matrícula já cadastrada")

    # Esse código acima é equivalente ao de baixo, mas é mais idiomático
    # if estudante_existe is not None:
    #     raise HTTPException(status_code=400, detail="Matrícula já cadastrada")

    # Se chegarmos nessa parte do código, isso significa que o usuário não existe e está quase pronto para
    # ser criado.
    # Agora, iremos fazer o seguinte:

    # - A matrícula não pode ser um número negativo, idade precisa ser um número maior ou igual a um.
    #   Logo, vamos checar isso

    novo_estudante = models.Estudante(**estudante.dict())
    matricula, idade = novo_estudante.matricula, novo_estudante.idade

    if matricula < 0:
        raise HTTPException(
            status_code=400, detail="Matrícula deve ser um número positivo e único"
        )

    if idade < 1:
        raise HTTPException(
            status_code=400, detail="Idade deve ser um número maior ou igual do que 1"
        )

    # Se chegarmos a essa parte do código, significa que os dados são únicos e válidos
    # Agora, estão prontos para serem adicionados ao banco de dados
    database.add(novo_estudante)
    database.commit()
    database.refresh(novo_estudante)
    return novo_estudante


@app.delete("/estudante/delete/{matricula}")
def delete_student(matricula: int, database: Session = Depends(get_database)):
    # Nesse código, se eu tentar remover um estudante que não existe, ele vai passar
    # Dessa maneira, vamos criar uma funcionalidade para checar se o estudante existe
    # Caso sim, então apague-o, caso não retorne um erro dizendo que o estudante não existe
    estudante_existe = (
        database.query(models.Estudante)
        .filter(
            models.Estudante.matricula == matricula,
        )
        .first()
    )

    if not estudante_existe:
        raise HTTPException(status_code=404, detail="Estudante não existe")

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
    # Se o estudante não existe, logo não tem como atualizar o que não existe
    student_from_db = (
        database.query(models.Estudante)
        .filter(
            models.Estudante.matricula == matricula,
        )
        .first()
    )
    if not student_from_db:
        raise HTTPException(status_code=404, detail="Matrícula inválida")

    # Agora, checar se os dados são válidos antes de atualizar
    matricula, idade = estudante.matricula, estudante.idade

    # Vamos lembrar que esses atributos podem ser "None" porque podemos atualizar apenas as fields
    # Que precisamos. Dessa maneira, precisamos checar se a field passada não é None antes de tentar
    # validar
    if matricula is not None:
        if matricula < 0:
            raise HTTPException(
                status_code=400,
                detail="Matrícula deve ser um número positivo e único",
            )

    if idade is not None:
        if idade < 1:
            raise HTTPException(
                status_code=400,
                detail="Idade deve ser um número maior ou igual do que 1",
            )

    updated_student = estudante.dict(exclude_unset=True)
    for key, value in updated_student.items():
        setattr(student_from_db, key, value)
    database.commit()
    database.refresh(student_from_db)
    return {"detail": "Estudante atualizado com sucesso"}
