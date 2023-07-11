"""Check Environment."""


from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from pip._internal.operations import freeze


@dag(start_date=days_ago(0), schedule=None)
def dag_check_environment() -> None:
    """Check Environment."""

    @task()
    def list_packages() -> None:
        """List all packages."""
        pkgs = freeze.freeze()
        for pkg in pkgs:
            print(pkg)

    list_packages()


dag_check_environment()
