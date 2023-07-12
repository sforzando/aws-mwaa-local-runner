"""Example of using AWS Redshift."""

from datetime import datetime, timezone
from os import getenv

from airflow import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.hooks.redshift_data import RedshiftDataHook
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator

REDSHIFT_CLUSTER_IDENTIFIER = getenv("REDSHIFT_CLUSTER_IDENTIFIER", "redshift_cluster_identifier")
REDSHIFT_DATABASE = getenv("REDSHIFT_DATABASE", "redshift_database")
REDSHIFT_DATABASE_USER = getenv("REDSHIFT_DATABASE_USER", "awsuser")

REDSHIFT_QUERY = """
SELECT table_schema,
       table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
      AND table_type = 'BASE TABLE'
ORDER BY table_schema,
         table_name;
            """
POLL_INTERVAL = 10


@task(task_id="output_results")
def output_query_results(statement_id: str) -> any:
    """Output the results of the query to the logs."""
    hook = RedshiftDataHook()
    return hook.conn.get_statement_result(
        Id=statement_id,
    )


with DAG(
    dag_id="example_redshift_data_execute_sql",
    start_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
) as dag:
    redshift_query = RedshiftDataOperator(
        task_id="redshift_query",
        cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
        database=REDSHIFT_DATABASE,
        db_user=REDSHIFT_DATABASE_USER,
        sql=REDSHIFT_QUERY,
        poll_interval=POLL_INTERVAL,
        await_result=True,
    )

    task_output = output_query_results(redshift_query.output)
