"""Airflow DAG for quotes scraping."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'quotes_scraper',
    default_args=default_args,
    description='Scrape quotes from websites and save to database',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    max_active_runs=1,
    tags=['scraping', 'quotes', 'data-pipeline'],
)

# Start task
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Database health check
db_check = PostgresOperator(
    task_id='check_database_health',
    postgres_conn_id='postgres_default',
    sql='SELECT 1',
    dag=dag,
)

# Scraping task
scrape_quotes = DockerOperator(
    task_id='scrape_quotes',
    image='web-scraper:latest',  # Your containerized scraper
    command='python -m scrapy crawl quotes_spider',
    environment={
        'DATABASE_HOST': '{{ var.value.database_host }}',
        'DATABASE_PORT': '{{ var.value.database_port }}',
        'DATABASE_NAME': '{{ var.value.database_name }}',
        'DATABASE_USER': '{{ var.value.database_user }}',
        'DATABASE_PASSWORD': '{{ var.value.database_password }}',
    },
    network_mode='bridge',
    dag=dag,
)

# Data validation


def validate_scraped_data():
    """Validate that quotes were scraped successfully."""
    from dags.utils.database_utils import validate_quotes_data

    # Your validation logic here
    result = validate_quotes_data()
    if not result:
        raise ValueError("Data validation failed")

    return "Data validation passed"


validation_task = PythonOperator(
    task_id='validate_scraped_data',
    python_callable=validate_scraped_data,
    dag=dag,
)

# End task
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Define task dependencies
start >> db_check >> scrape_quotes >> validation_task >> end
