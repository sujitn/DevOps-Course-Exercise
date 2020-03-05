# Pull official Python base image
FROM python:3.8-slim-buster

# Update package managers
RUN apt-get update && pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy app project files
WORKDIR /home/app
COPY . .

ENTRYPOINT ["gunicorn", "app:app"]
CMD ["--config gunicorn.conf.py"]
