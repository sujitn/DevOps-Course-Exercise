FROM python:3.8.6-buster as base

ENV PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	POETRY_VERSION=1.1.0
RUN pip install "poetry==$POETRY_VERSION"

COPY . ./app
WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

FROM base as production
RUN pip install gunicorn
EXPOSE 8000
ENTRYPOINT ["./entrypoint_prod.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["./entrypoint_dev.sh"]