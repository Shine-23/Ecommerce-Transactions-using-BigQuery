from google.cloud import bigquery

# Initialize BigQuery Client
client = bigquery.Client()

def run_query(query):
    """
    Executes a BigQuery SQL query and returns the result as a list of dictionaries.
    """
    try:
        query_job = client.query(query)  # Make API request
        results = query_job.result()  # Wait for query to complete
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Error running query: {e}")
        return []
