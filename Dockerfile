# Pull official Python base image
FROM python:3.8-slim-buster as dev

# Update package managers
RUN apt-get update && pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy app project files
WORKDIR /home/app
COPY . .

# Use Flask in development mode
ENV FLASK_ENV=development

ENTRYPOINT ["flask", "run"]
CMD ["--host=0.0.0.0", "--port=80"]


##################################################
# Testing image based on dev image
FROM dev as test

# Install packages required for testing
RUN pip install pytest watchdog[watchmedo]

# Configure Pytest options
ENV PYTEST_ADDOPTS="--color=yes"

ENTRYPOINT ["watchmedo", "auto-restart", "--recursive", "--directory=.", "--pattern=*.py", "--ignore-patterns=*/.*"]
CMD ["pytest"]


##################################################
# Production image based on dev image
FROM dev as production

# Use Flask in production mode
ENV FLASK_ENV=production

ENTRYPOINT ["gunicorn", "app:app"]
CMD ["--config gunicorn.conf.py"]
