from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


def _demo_task():
    print("Hello World!!")

    
dag = DAG(
    dag_id = 'demo_dag',
    catchup = False,
    start_date = days_ago(2),
    schedule_interval = '@daily'
)

demo_task = PythonOperator(
    task_id = 'demo_task',
    dag= dag,
    python_callable = _demo_task
)