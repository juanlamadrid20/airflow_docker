
# Step-1: Import modules
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator

# Step-2: Define default args
default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 1, 25),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# Step-3: Instantiate DAGs --- or creating a DAG object
dag = DAG(dag_id='DAG-1',
          default_args=default_args,
          catchup=False,
          schedule_interval='@once'
          )

# Step-4: Define Tasks
start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

# Step-5: Define dependencies
start >> end
