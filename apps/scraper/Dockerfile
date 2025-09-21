# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/code \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock /code/

# Copy libs directory for workspace dependencies
COPY ./apps /code/apps
COPY ./libs /code/libs

# Install Python dependencies
RUN cd /code/apps/scraper && uv sync --frozen

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash scraper && \
    chown -R scraper:scraper /code
USER scraper

# Set the default command
CMD ["python", "-m", "scrapy", "crawl", "quotes_spider"]
