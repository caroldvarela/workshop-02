import requests
import pandas as pd
import json
import logging
from src.extract.read_grammy import read_grammy_db
from src.extract.read_spotify import read_spotify_csv
from src.transform.transform_grammy import TransformGrammy
from src.transform.transform_spotify import TransformSpotify


def read_spotify(**kwargs):
   logging.info("Extracting Spotify data")
   json_data = read_spotify_csv()
   if json_data is not None:
       logging.info("Spotify data extracted successfully.")
   else:
       logging.error("Failed to extract Spotify data.")
   return json_data


def transform_spotify(**kwargs):
   logging.info("Transforming data spotify")
   ti = kwargs["ti"]
   str_data = ti.xcom_pull(task_ids="read_spotify")
   json_data = json.loads(str_data)
  
   transformer = TransformSpotify(pd.DataFrame(json_data))
   transformer.unnamed_to_id()
   transformer.drop_nan_records()
   transformer.normalize_data()
   transformer.filter_max_popularity_tracks()
   transformed_data = transformer.df.to_json(orient='records')
   logging.info(f"Transformed data: {transformer.df.head()}")
   return transformed_data


def read_grammy(**kwargs):
   logging.info("Extracting Grammy data")
   json_data = read_grammy_db()
   if json_data is not None:
       logging.info("Grammy data extracted successfully.")
   else:
       logging.error("Failed to extract Grammy data.")
  
   return json_data


def transform_grammy(**kwargs):
   logging.info("Transforming data grammy")
   ti = kwargs["ti"]
   str_data = ti.xcom_pull(task_ids="transform_spotify")
   json_data = json.loads(str_data)
  
   transformer = TransformGrammy(pd.DataFrame(json_data))
   transformer.insert_ids()
   transformer.remove_unwanted_grammmy_columns()
   transformer.remove_na_nominees()
   transformer.extract_artists()
   transformer.remove_parentheses_from_artists()
   transformer.mark_winners()
   transformer.filter_winners()
  
   transformed_data = transformer.df.to_json(orient='records')
   logging.info(f"Transformed data: {transformer.df.head()}")
   return transformed_data




def load(**kwargs):
   logging.info("Starting load process")
   ti = kwargs["ti"]
   str_data = ti.xcom_pull(task_ids="transform_grammy")
   json_data = json.loads(str_data)
   data = pd.json_normalize(data=json_data)
   logging.info( f"data to load is: {data}")
   logging.info("Loading data")
   logging.info( "data loaded in: table_name")