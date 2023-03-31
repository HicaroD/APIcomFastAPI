# APIswithFastAPI

Código utilizado no minicurso de como criar APIs usando Python e FastAPI

## Pré-requisitos

Para conseguir seguir o minicurso, você precisará possuir algumas bibliotecas instaladas, use os comandos abaixo:

Nesse primeiro comando, iremos criar um ambiente virtual para adicionar as bibliotecas necessárias:

```bash
python -m venv .env && source .env/bin/activate
```

Agora, vamos instalar as bibliotecas dentro de nosso ambiente virtual:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy
```

Obs.: **Não tenho certeza se o primeiro comando funciona no Windows.**
