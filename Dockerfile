FROM python:3.8.5-buster as base
COPY . .
RUN pip install "poetry==1.0.10" \
  && poetry install

FROM base as production
RUN pip install gunicorn flask
EXPOSE 8000
ENTRYPOINT ["./run-prod.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["./run-dev.sh"]