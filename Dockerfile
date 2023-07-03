FROM python:3.10-slim as base

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip \
    && apt-get update \
    && apt-get install -y curl build-essential

FROM base as poetry

ENV POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

ENV PATH="${POETRY_HOME}/bin:$PATH"
RUN poetry config virtualenvs.create ${POETRY_VIRTUALENVS_CREATE}
RUN poetry config virtualenvs.in-project ${POETRY_VIRTUALENVS_IN_PROJECT}

FROM poetry as build

WORKDIR /app

# copy project
COPY src ./src

# install dependencies POETRY
COPY pyproject.toml ./pyproject.toml
RUN poetry install

CMD ["python", "main.py"]
