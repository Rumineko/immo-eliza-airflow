from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from collection.main import collection
from machinelearning.preprocess import cleaning
from machinelearning.train import train

current_dir = os.path.dirname(__file__)

my_dag = DAG(
    dag_id="immo_eliza",
    start_date=datetime(2024, 4, 25),
    schedule="@daily",
)

collection_task = PythonOperator(
    task_id="collection", python_callable=collection, dag=my_dag
)

cleaning_task = PythonOperator(task_id="cleaning", python_callable=cleaning, dag=my_dag)

training_task = PythonOperator(task_id="training", python_callable=train, dag=my_dag)


collection_task >> cleaning_task >> training_task
