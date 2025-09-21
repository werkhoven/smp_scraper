# Web Scraper

A web scraping project using Scrapy and uv package manager, designed to run in a dev container.

## 🐳 Dev Container Setup

This project is configured to run in a dev container for a consistent development environment.

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. **Clone the repository** (if not already done)
2. **Open in VS Code**
3. **Reopen in Container**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Dev Containers: Reopen in Container"
   - Select the command and wait for the container to build

The dev container will automatically:

- Install all Python dependencies
- Set up the development environment
- Configure VS Code extensions
- Mount your workspace

## 📁 Project Structure

```
web_scraper/
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # VS Code dev container settings
│   └── Dockerfile          # Container image definition
├── apps/                   # Application code
│   └── scraper/           # Scrapy application
│       ├── spiders/       # Spider implementations
│       ├── items.py       # Data models
│       ├── pipelines.py   # Data processing pipelines
│       ├── middlewares.py # Custom middleware
│       ├── settings.py    # Scrapy settings
│       ├── Dockerfile     # Scraper container definition
│       └── README.md      # Scraper documentation
├── libs/                   # Shared libraries
│   └── db/                # Database library
│       ├── src/db/        # Database code
│       └── pyproject.toml # DB library dependencies
├── dags/                   # Airflow DAGs
│   ├── quotes_scraper_dag.py # Main scraping DAG
│   ├── utils/             # DAG utility functions
│   └── README.md          # DAG documentation
├── scripts/                # Helper scripts
├── tests/                  # Test files
├── docker-compose.yml      # Docker services
├── Makefile               # Development commands
└── pyproject.toml         # Project dependencies and config
```

## 🚀 Usage

### Running Spiders

```bash
# Run the example spider
make run-spider

# Run with debug output
make run-spider-debug

# List available spiders
make list-spiders
```

### Airflow DAGs

The project includes Airflow DAGs for orchestrating the scraping process:

```bash
# Deploy DAGs to managed Airflow service
# (See dags/README.md for specific instructions)

# For Google Cloud Composer:
gsutil cp dags/quotes_scraper_dag.py gs://your-composer-bucket/dags/

# For Amazon MWAA:
aws s3 cp dags/quotes_scraper_dag.py s3://your-mwaa-bucket/dags/
```

### Development Commands

```bash
# Install dependencies
make install

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Lint code
make lint

# Clean up generated files
make clean
```

## 🐳 Docker Services

The project includes optional Docker services for a complete development environment:

### Database (PostgreSQL)

```bash
# Start PostgreSQL database
docker-compose --profile database up -d postgres

# Connect to database
docker-compose exec postgres psql -U scraper -d scraper_db
```

### Cache (Redis)

```bash
# Start Redis cache
docker-compose --profile cache up -d redis

# Connect to Redis
docker-compose exec redis redis-cli
```

### Jupyter Notebook

```bash
# Start Jupyter notebook
docker-compose --profile jupyter up -d jupyter

# Access at http://localhost:8888
```

### All Services

```bash
# Start all services
docker-compose --profile database --profile cache --profile jupyter up -d
```

## ⚙️ Configuration

### Environment Variables

Copy the environment template and configure your settings:

```bash
cp env.example .env
# Edit .env with your configuration
```

### Key Settings

- `DOWNLOAD_DELAY`: Delay between requests (seconds)
- `CONCURRENT_REQUESTS`: Number of concurrent requests
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `DATA_DIR`: Directory for output files

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_spiders.py -v

# Run with coverage
make test-cov
```

## 📊 Monitoring

### Scrapy Telnet Console

- Access: `telnet localhost 8080`
- Commands: `stats`, `list`, `close`

### Logs

- Location: `logs/scraper.log`
- Real-time: `tail -f logs/scraper.log`

## 🔧 Troubleshooting

### Container Issues

```bash
# Rebuild container
docker-compose build --no-cache

# View container logs
docker-compose logs web-scraper

# Access container shell
docker-compose exec web-scraper bash
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Dependency Issues

```bash
# Reinstall dependencies
make clean
uv sync
```

## 📚 Resources

- [Scrapy Documentation](https://docs.scrapy.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Dev Containers Documentation](https://code.visualstudio.com/docs/remote/containers)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
