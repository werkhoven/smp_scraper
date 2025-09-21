#!/bin/bash

# Database migration script for Docker container

set -e

echo "Running database migrations..."

# Change to the database directory
cd /app/libs/db/src/db

# Run migrations
python -m alembic upgrade head

echo "Migrations completed successfully!"
