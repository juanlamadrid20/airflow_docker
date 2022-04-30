FROM apache/airflow:2.0.0-python3.8

WORKDIR /opt/airflow

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./dags ./dags
