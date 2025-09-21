# Makefile for web scraper Docker operations

.PHONY: help build run stop clean logs shell test

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build the Docker image"
	@echo "  run       - Run the scraper with docker-compose"
	@echo "  run-prod  - Run with production docker-compose"
	@echo "  stop      - Stop all containers"
	@echo "  clean     - Remove containers and images"
	@echo "  logs      - Show logs from scraper container"
	@echo "  shell     - Open shell in scraper container"
	@echo "  test      - Run tests in container"
	@echo "  migrate   - Run database migrations"

# Build the Docker image
build:
	docker build -f apps/scraper/Dockerfile -t web-scraper:latest .

# Run with development docker-compose
run:
	docker-compose up --build

# Run with production docker-compose
run-prod:
	docker-compose -f docker-compose.prod.yml up --build

# Stop all containers
stop:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

# Clean up containers and images
clean:
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose -f docker-compose.prod.yml down --rmi all --volumes --remove-orphans
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f scraper

# Open shell in scraper container
shell:
	docker-compose exec scraper /bin/bash

# Run tests
test:
	docker-compose exec scraper python -m pytest

# Run database migrations
migrate:
	docker-compose exec scraper bash -c "cd libs/db/src/db && python -m alembic upgrade head"

# Run scraper with specific spider
crawl:
	docker-compose exec scraper python -m scrapy crawl $(SPIDER)

# Example: make crawl SPIDER=quotes_spider