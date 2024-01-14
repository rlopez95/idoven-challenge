FROM python:3.11-slim-bullseye

WORKDIR /code

COPY pyproject.toml /code
COPY poetry.lock /code

RUN pip install poetry

RUN poetry install

COPY . /code

CMD ["poetry", "run", "uvicorn", "idoven_app.main:app", "--host", "0.0.0.0", "--port", "8080"]