FROM python:3.13

WORKDIR /url_shortcutter

COPY pyproject.toml poetry.lock README.md /url_shortcutter/
COPY ./url_shortcutter /url_shortcutter/url_shortcutter

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install


COPY ./alembic/. /url_shortcutter/alembic/.
COPY alembic-db.ini /url_shortcutter/alembic.ini

CMD ["alembic", "upgrade", "head"]

EXPOSE 8000

CMD ["uvicorn", "url_shortcutter.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
