FROM python:3.9.6

RUN pip install --upgrade pip
COPY ./poetry.lock ./
COPY ./pyproject.toml ./
COPY ./src ./src
RUN pip install poetry
RUN poetry install --without dev
