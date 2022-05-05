from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

dag = DAG(
    dag_id = 'demo_dag',
    catchup = False,
    start_date = days_ago(2),
    schedule_interval = '@daily'
)

def _demo_task():
    print("Hello World")

demo_task = PythonOperator(
    task_id = 'demo_task',
    dag= dag,
    python_callable = _demo_task
)