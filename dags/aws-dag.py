import os

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3_bucket import S3CreateBucketOperator, S3DeleteBucketOperator
from airflow.utils.dates import days_ago

import awswrangler as wr
from datetime import datetime
import pandas as pd
import requests
from typing import Any, Dict

import boto3

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'ru-test-airflow-12345')
boto3.setup_default_session(
    region_name="us-east-1", 
    aws_access_key_id="ABCXXXXXXYZ", 
    aws_secret_access_key="ABCXXXXXXYZ"
)

def extract_prices() -> Dict[str, Any]:
    url = (
        "https://min-api.cryptocompare.com/data/pricemulti?"
        "fsyms=BTC,ETH,REP,DASH&tsyms=USD"
    )
    response = requests.get(url)
    prices = response.json()
    print(f"Received data: {prices}")
    return prices


def transform_prices(json_data: Dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(json_data)
    now = datetime.utcnow()
    print(f"Adding a column TIME with current time: {now}")
    df["TIME"] = now
    return df.reset_index(drop=True)

def load_prices(df: pd.DataFrame) -> None:
    table_name = "crypto-airflow"
    wr.s3.to_parquet(
        df=df,
        path="s3://airflow-12345-bucket/crypto/",
        dataset=True,
        mode="append",
        database="default",
        table=table_name,
    )
    print(f"Table {table_name} in Athena data lake successfully updated 🚀")


def real_time_flow():
    raw_prices = extract_prices()
    transformed_data = transform_prices(raw_prices)
    load_prices(transformed_data)

with DAG(
    dag_id='s3_bucket_dag',
    schedule_interval=None,
    start_date=days_ago(2),
    max_active_runs=1,
    tags=['example'],
) as dag:

    # [START howto_operator_s3_bucket]
    create_bucket = S3CreateBucketOperator(
        task_id='s3_bucket_dag_create',
        bucket_name="airflow-12345-bucket",
        region_name='us-east-1',
    )

    real_time_flow = PythonOperator(
        task_id="s3_realtime_flow", 
        python_callable=real_time_flow
    )

    # delete_bucket = S3DeleteBucketOperator(
    #     task_id='s3_bucket_dag_delete',
    #     bucket_name="airflow-12345-bucket",
    #     force_delete=True,
    # )
    # [END howto_operator_s3_bucket]

    # create_bucket >> add_keys_to_bucket >> delete_bucket
    create_bucket >> real_time_flow