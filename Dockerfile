FROM python:3.13

WORKDIR /url_shortcutter

COPY pyproject.toml poetry.lock README.md /url_shortcutter/
COPY ./url_shortcutter /url_shortcutter/url_shortcutter

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install && \
    apt-get update && \
    apt-get install -y netcat-openbsd


COPY ./alembic/. /url_shortcutter/alembic/.
COPY alembic-db.ini /url_shortcutter/alembic.ini

COPY entrypoint.sh /url_shortcutter/entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
