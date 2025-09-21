# Airflow DAGs

This directory contains Airflow DAGs for orchestrating the web scraper application.

## Structure

```
dags/
├── quotes_scraper_dag.py    # Main quotes scraping DAG
├── utils/                   # Utility functions for DAGs
│   ├── __init__.py
│   └── database_utils.py    # Database utility functions
└── README.md               # This file
```

## DAGs

### quotes_scraper_dag.py
- **Schedule**: Daily at 2 AM
- **Tasks**:
  1. `start` - Dummy start task
  2. `check_database_health` - Verify database connectivity
  3. `scrape_quotes` - Run the containerized scraper
  4. `validate_scraped_data` - Validate scraped data
  5. `end` - Dummy end task

## Deployment

### For Managed Airflow Services:

#### Google Cloud Composer:
```bash
# Upload DAG files
gsutil cp dags/quotes_scraper_dag.py gs://your-composer-bucket/dags/
gsutil cp -r dags/utils/ gs://your-composer-bucket/dags/
```

#### Amazon MWAA:
```bash
# Upload to S3
aws s3 cp dags/quotes_scraper_dag.py s3://your-mwaa-bucket/dags/
aws s3 cp -r dags/utils/ s3://your-mwaa-bucket/dags/
```

### For Local Development:
```bash
# Use docker-compose with Airflow
docker-compose -f docker-compose.airflow.yml up -d
```

## Configuration

### Airflow Variables (set in Airflow UI or CLI):
- `database_host` - Database host
- `database_port` - Database port (default: 5432)
- `database_name` - Database name
- `database_user` - Database user
- `database_password` - Database password

### Airflow Connections:
- `postgres_default` - PostgreSQL connection for database operations

## Usage

### Setting Variables:
```bash
# Google Cloud Composer
gcloud composer environments run your-env \
    --location us-central1 \
    variables set -- database_host your-db-host

# Amazon MWAA
aws mwaa create-environment \
    --name your-env \
    --airflow-configuration-options '{"core.database_host":"your-db-host"}'
```

### Running DAGs:
1. Upload DAG files to your Airflow environment
2. Set required variables and connections
3. Enable the DAG in the Airflow UI
4. Monitor execution in the Airflow UI

## Development

### Local Testing:
```bash
# Test DAG syntax
python dags/quotes_scraper_dag.py

# Test with Airflow CLI
airflow dags test quotes_scraper 2024-01-01
```

### Adding New DAGs:
1. Create new DAG file in this directory
2. Follow the same structure and naming conventions
3. Add utility functions to `utils/` if needed
4. Update this README

## Best Practices

1. **Keep DAGs Simple**: Focus on orchestration, not business logic
2. **Use Variables**: Store configuration in Airflow Variables
3. **Error Handling**: Implement proper retry and failure handling
4. **Monitoring**: Set up alerts and notifications
5. **Testing**: Test DAGs locally before deployment
6. **Documentation**: Document DAG purpose and configuration
