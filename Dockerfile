# Use Python 3.13 slim base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry --version

# Set PATH for Poetry
ENV PATH="${PATH}:/opt/poetry/bin"

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY dox_agent/ ./dox_agent/
COPY README.md ./

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
RUN poetry install --no-dev

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "dox-agent"] 