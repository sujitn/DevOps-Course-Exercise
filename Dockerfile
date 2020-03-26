# Use official Python base image
FROM python:3.8-slim-buster as base

# Update package managers
RUN apt-get update && pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy app project files
WORKDIR /home/app
COPY . .


##################################################
# Development image (uses Flask development server)
FROM base as development

# Use Flask in development mode
ENV FLASK_ENV=development

ENTRYPOINT ["flask", "run"]
CMD ["--host=0.0.0.0", "--port=80"]


##################################################
# Testing image (uses Watchdog to run Pytest whenever files change)
FROM base as test

# Install packages required for testing
RUN pip install pytest watchdog[watchmedo]

# Configure Pytest options
ENV PYTEST_ADDOPTS="--color=yes"

ENTRYPOINT ["watchmedo", "auto-restart", "--recursive", "--directory=.", "--pattern=*.py", "--ignore-patterns=*/.*"]
CMD ["pytest"]


##################################################
# Production image (uses Gunicorn as the WSGI server)
FROM base as production

# Use Flask in production mode
ENV FLASK_ENV=production

ENTRYPOINT ["gunicorn", "app:app"]
CMD ["--config gunicorn.conf.py"]
