# APIswithFastAPI

Código utilizado no módulo 3 e 4 do minicurso de como criar APIs usando Python e FastAPI.
Caso queira saber onde estão os códigos do primeiro e segundo módulo, acesse 
[esse link](https://github.com/Rodrigo021/Minicurso-FastAPI).

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

Para ter acesso ao banco de dados SQLite, o qual será usado a partir do módulo 3 do minicurso, faça o download usando [esse link](https://drive.google.com/file/d/1CV5w5L3wMR-00BwVyVsS0nKWeKWeZK74/view?usp=share_link) e cole na pasta raiz do seu projeto (onde ficará seus arquivos `.py` e etc).

