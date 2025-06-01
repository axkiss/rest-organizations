FROM python:3.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore
ENV CURL_CA_BUNDLE ""
ENV POETRY_VIRTUALENVS_CREATE true
ENV PATH "${PATH}:/root/.local/bin"



WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN set -ex; \
    apk update; \
    apk add --no-cache --virtual build-deps \
        curl \
        git \
        gcc \
        libpq \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --user poetry==1.6 \
    && poetry install --no-interaction --no-ansi \
    && apk del --no-cache build-deps

RUN ln -sf $(poetry env info -e) /python
COPY . /app/

EXPOSE 8000/tcp

RUN chmod +x entrypoint.*