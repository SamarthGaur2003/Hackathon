from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import os

# Absolute path to …/data on the host
BASE_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR  = os.path.join(BASE_DIR, 'data')          # e.g. /home/ubuntu/Hackathon/weather‑pipeline/data
VOLUMEARG = f'"{DATA_DIR}":/data'                   # quoted for safety

with DAG(
    dag_id          = 'weather_pipeline',
    start_date      = datetime(2023, 1, 1),
    schedule_interval='@hourly',
    catchup         = False,
    description     = 'Ingest then process weather data',
) as dag:

    ingest = BashOperator(
        task_id      = 'ingest',
        bash_command = f'docker run --rm -v {VOLUMEARG} weather-ingest',
    )

    process = BashOperator(
        task_id      = 'process',
        bash_command = f'docker run --rm -v {VOLUMEARG} weather-process',
    )

    ingest >> process


