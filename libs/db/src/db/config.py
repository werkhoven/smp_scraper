
"""Database configuration."""

import os

# Database configuration
postgres_host: str = os.getenv("DATABASE_HOST", "localhost")
postgres_port: str = os.getenv("DATABASE_PORT", "5432")
postgres_database: str = os.getenv("DATABASE_NAME", "scraper_db")
postgres_username: str = os.getenv("DATABASE_USER", "scraper")
postgres_password: str = os.getenv("DATABASE_PASSWORD", "scraper_password")
postgres_schema: str = os.getenv("POSTGRES_SCHEMA", "public")

# Connection string and arguments used by SQLAlchemy
db_url = f"postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}"
