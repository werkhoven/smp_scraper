#!/usr/bin/env bash
set -e

echo "🚀 Setting up web scraper development environment..."

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv venv --python 3.11
uv sync

# Start PostgreSQL database with Docker Compose in background
echo "🐘 Starting PostgreSQL database in background..."
docker-compose up -d postgres

echo "✅ Database startup initiated!"
echo "   Database will be ready shortly. You can check status with:"
echo "   docker-compose ps"
echo "   docker-compose logs postgres"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "   Please review and update .env file with your settings"
fi

echo "🎉 Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "   - Review and update .env file if needed"
echo "   - Run 'docker-compose ps' to check database status"
echo "   - Run 'docker-compose logs postgres' to view database logs"
echo "   - Start developing your web scraper!"

