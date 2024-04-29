from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
eliza_dir = os.path.join(current_dir, "eliza")
machinelearning_dir = os.path.join(eliza_dir, "machinelearning")
sys.path.append(machinelearning_dir)


from preprocess import cleaning
from train import train

collect_command = """
cd ../../../opt/airflow/dags/eliza/collection/scrapy
scrapy crawl immoweb
"""

my_dag = DAG(
    dag_id="immo_eliza",
    start_date=datetime(2024, 4, 25),
    schedule="@daily",
)

collection_task = BashOperator(
    task_id="collection", bash_command=collect_command, dag=my_dag
)

cleaning_task = PythonOperator(task_id="cleaning", python_callable=cleaning, dag=my_dag)

training_task = PythonOperator(task_id="training", python_callable=train, dag=my_dag)


collection_task >> cleaning_task >> training_task
