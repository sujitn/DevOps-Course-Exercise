FROM python:3.8.5-buster as base
RUN pip install "poetry==1.0.10"
COPY . ./app
WORKDIR /app
RUN poetry install

FROM base as production
RUN pip install gunicorn flask
EXPOSE 8000
ENTRYPOINT ["./run-prod.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["./run-dev.sh"]