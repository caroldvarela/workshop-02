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
  'start_date': datetime(2023, 12, 31),
  'email': ['airflow@example.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 5,
  'retry_delay': timedelta(minutes=2)
}


with DAG(
  'dag_workshop2',
  default_args=default_args,
  description='DAG for the ETL process of Spotify and Grammy',
  schedule_interval='@daily',
) as dag:



  read_spotify_task = PythonOperator(
      task_id='read_spotify',
      python_callable=extract_spotify,

  )


  transform_spotify_task = PythonOperator(
      task_id='transform_spotify',
      python_callable=transform_spotify,

  )




  read_grammy_task = PythonOperator(
      task_id='read_grammy',
      python_callable=extract_grammy,

  )




  transform_grammy_task = PythonOperator(
      task_id='transform_grammy',
      python_callable=transform_grammy,

  )



  merge_task = PythonOperator(
      task_id='merge',
      python_callable=merge_data,
 
  )

  load_task = PythonOperator(
      task_id='load',
      python_callable=load_data_to_db,

  )

  store_task = PythonOperator(
      task_id='store',
      python_callable=store_drive,

  )




  read_spotify_task >> transform_spotify_task
  read_grammy_task >> transform_grammy_task
  transform_spotify_task >> merge_task
  transform_grammy_task >> merge_task
  merge_task >> load_task
  load_task >> store_task