from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

def create_dag():
    with DAG(
        dag_id="weather_pipeline",
        start_date=datetime(2023, 1, 1),
        schedule_interval="@daily",
        catchup=False
    ) as dag:

        ingest = BashOperator(
            task_id="ingest",
            bash_command="docker run --rm -v $PWD/data:/data weather-ingest"
        )

        process = BashOperator(
            task_id="process",
            bash_command="docker run --rm -v $PWD/data:/data weather-process"
        )

        visualize = BashOperator(
            task_id="visualize",
            bash_command="docker run --rm -v $PWD/data:/data -p 5000:5000 weather-visualize"
        )

        ingest >> process >> visualize

    return dag

globals()["weather_pipeline"] = create_dag()