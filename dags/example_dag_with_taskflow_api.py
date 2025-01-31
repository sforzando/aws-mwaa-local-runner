"""DAG exhibiting task flow paradigm in airflow 2.0.

Note:
    https://airflow.apache.org/docs/apache-airflow/2.0.2/tutorial_taskflow_api.html
"""

import json
import sys

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
}


@dag(
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(2),
    tags=["example"],
)
def dag_with_taskflow_api() -> any:
    """### TaskFlow API Tutorial Documentation.

    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.

    Note:
        https://airflow.apache.org/docs/stable/tutorial_taskflow_api.html
    """

    @task()
    def extract() -> any:
        """Extract task.

        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        return json.loads(data_string)

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict) -> any:
        """Transform task.

        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float) -> any:
        """Load task.

        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """
        print("Total order value is: %.2f" % total_order_value)
        print(f"Python Version: {sys.version}")

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


dag_with_taskflow_api = dag_with_taskflow_api()
