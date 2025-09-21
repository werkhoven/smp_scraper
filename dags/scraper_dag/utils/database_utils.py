"""Database utility functions for Airflow DAGs."""

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable


def validate_quotes_data():
    """Validate that quotes were scraped successfully.

    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Get database connection
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')

        # Check if quotes were added recently (last 24 hours)
        query = """
        SELECT COUNT(*) 
        FROM quotes 
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        """

        result = postgres_hook.get_first(query)
        quote_count = result[0] if result else 0

        # Validate that we have quotes
        if quote_count > 0:
            print(
                f"Validation passed: {quote_count} quotes found in last 24 hours")
            return True
        else:
            print("Validation failed: No quotes found in last 24 hours")
            return False

    except Exception as e:
        print(f"Validation error: {e}")
        return False


def get_quote_statistics():
    """Get statistics about scraped quotes.

    Returns:
        dict: Statistics about quotes
    """
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')

        # Get total quotes count
        total_query = "SELECT COUNT(*) FROM quotes"
        total_result = postgres_hook.get_first(total_query)
        total_quotes = total_result[0] if total_result else 0

        # Get quotes by author
        author_query = """
        SELECT author, COUNT(*) as count 
        FROM quotes 
        GROUP BY author 
        ORDER BY count DESC 
        LIMIT 10
        """
        author_results = postgres_hook.get_records(author_query)

        # Get recent quotes
        recent_query = """
        SELECT COUNT(*) 
        FROM quotes 
        WHERE created_at >= NOW() - INTERVAL '7 days'
        """
        recent_result = postgres_hook.get_first(recent_query)
        recent_quotes = recent_result[0] if recent_result else 0

        return {
            'total_quotes': total_quotes,
            'recent_quotes': recent_quotes,
            'top_authors': dict(author_results) if author_results else {}
        }

    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {}


def cleanup_old_quotes(days_to_keep=30):
    """Clean up old quotes from the database.

    Args:
        days_to_keep (int): Number of days to keep quotes

    Returns:
        int: Number of quotes deleted
    """
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')

        delete_query = """
        DELETE FROM quotes 
        WHERE created_at < NOW() - INTERVAL '%s days'
        """ % days_to_keep

        result = postgres_hook.run(delete_query)
        return result.rowcount if hasattr(result, 'rowcount') else 0

    except Exception as e:
        print(f"Error cleaning up quotes: {e}")
        return 0
