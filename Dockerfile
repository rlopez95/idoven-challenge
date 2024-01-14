FROM python:3.10

WORKDIR /code

COPY pyproject.toml /code
COPY poetry.lock /code

RUN pip install poetry

RUN poetry install

COPY . /code

CMD ["poetry", "run", "uvicorn", "idoven.main:app", "--host", "0.0.0.0", "--port", "8080"]