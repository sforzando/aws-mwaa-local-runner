"""Example of using AWS Lambda."""

import json
from datetime import datetime, timedelta, timezone
from os import getenv

from airflow import DAG
from airflow.providers.amazon.aws.operators.aws_lambda import (
    AwsLambdaInvokeFunctionOperator,
)

LAMBDA_FUNCTION_NAME = getenv("LAMBDA_FUNCTION_NAME", "test-function")

SAMPLE_EVENT = json.dumps({"SampleEvent": {"SampleData": {"Name": "XYZ", "DoB": "1993-01-01"}}})

with DAG(
    dag_id="example_lambda",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
    dagrun_timeout=timedelta(minutes=60),
    tags=["example"],
    catchup=False,
) as dag:
    setup__invoke_lambda_function = AwsLambdaInvokeFunctionOperator(
        task_id="setup__invoke_lambda_function",
        function_name=LAMBDA_FUNCTION_NAME,
        payload=SAMPLE_EVENT,
    )
