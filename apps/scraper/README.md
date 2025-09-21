# Web Scraper Docker Setup

This directory contains the Docker configuration for the web scraper application.

## Files

- `Dockerfile` - Docker image definition for the scraper
- `.dockerignore` - Files to exclude from Docker build context
- `README.md` - This file

## Building and Running

### Using Docker Compose (Recommended)

From the project root:

```bash
# Build and run with database
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Using Make Commands

From the project root:

```bash
# Build the image
make build

# Run with docker-compose
make run

# Stop services
make stop

# View logs
make logs

# Open shell in container
make shell

# Run migrations
make migrate
```

### Manual Docker Commands

```bash
# Build the image
docker build -f apps/scraper/Dockerfile -t web-scraper:latest .

# Run the container (requires external database)
docker run --rm -e DATABASE_HOST=host.docker.internal web-scraper:latest
```

## Environment Variables

The scraper uses the following environment variables:

- `DATABASE_HOST` - Database host (default: postgres)
- `DATABASE_PORT` - Database port (default: 5432)
- `DATABASE_NAME` - Database name (default: scraper_db)
- `DATABASE_USER` - Database user (default: scraper)
- `DATABASE_PASSWORD` - Database password (default: scraper_password)

## Development

For development, you can override the default command:

```bash
# Run with custom command
docker-compose run --rm scraper python -m scrapy shell

# Run specific spider
docker-compose run --rm scraper python -m scrapy crawl quotes_spider
```

## Production

For production deployment with Airflow, use the DockerOperator:

```python
from airflow.operators.docker_operator import DockerOperator

scrape_task = DockerOperator(
    task_id='scrape_quotes',
    image='web-scraper:latest',
    command='python -m scrapy crawl quotes_spider',
    environment={
        'DATABASE_HOST': 'your-db-host',
        'DATABASE_NAME': 'your-db-name',
        # ... other env vars
    },
    dag=dag,
)
```
