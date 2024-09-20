import sys
import os
from dotenv import load_dotenv

load_dotenv()
work_dir = os.getenv('WORK_DIR')

sys.path.append(work_dir)

from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dags.etl import *




default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2024, 12, 31),
  'email': ['airflow@example.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1)
}




with DAG(
  'dag_workshop2',
  default_args=default_args,
  description='DAG para el proceso ETL de Spotify y Grammy',
  schedule_interval='@daily',
) as dag:




  read_spotify_task = PythonOperator(
      task_id='read_spotify',
      python_callable=read_spotify,
      provide_context=True,
  )




  transform_spotify_task = PythonOperator(
      task_id='transform_spotify',
      python_callable=transform_spotify,
      provide_context=True,
  )




  read_grammy_task = PythonOperator(
      task_id='read_grammy',
      python_callable=read_grammy,
      provide_context=True,
  )




  transform_grammy_task = PythonOperator(
      task_id='transform_grammy',
      python_callable=transform_grammy,
      provide_context=True,
  )




  load_task = PythonOperator(
      task_id='load',
      python_callable=load,
      provide_context=True,
  )




  read_spotify_task >> transform_spotify_task
  read_grammy_task >> transform_grammy_task
  transform_spotify_task >> load_task
  transform_grammy_task >> load_task