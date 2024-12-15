import time
from google.cloud import bigquery

client = bigquery.Client()

def query_with_retry(query, retries=3, delay=2):
    """
    Executes a BigQuery SQL query with retry logic.
    Args:
        query (str): SQL query to execute.
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.
    Returns:
        list: Query results as a list of dictionaries.
    Raises:
        Exception: If the query fails after all retries.
    """
    for attempt in range(retries):
        try:
            query_job = client.query(query)  # Make API request
            results = query_job.result()  # Wait for query to complete
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Query failed on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Query failed after all retries.")
