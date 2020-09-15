FROM python:3.8.5-buster

COPY . .

RUN pip install "poetry==1.0.10" \
  && poetry install

EXPOSE 5000

ENTRYPOINT ["./run.sh"]