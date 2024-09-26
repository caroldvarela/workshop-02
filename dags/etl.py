import pandas as pd
import json
import logging
from src.extract.read_grammy import read_grammy_db
from src.extract.read_spotify import read_spotify_csv
from src.transform.transform_grammy import TransformGrammy
from src.transform.transform_spotify import TransformSpotify
from src.merge.merge import MergeData
from src.load.load_to_database import load_data
from src.store.store import authenticate, upload_file
import io

def extract_spotify(**kwargs):
    logging.info("Starting data extraction for Spotify")
    try:
        spotify_data = read_spotify_csv()
        if spotify_data is None:
            logging.error("Failed to extract Spotify data.")
            return None
        logging.info("Spotify data extracted successfully.")
    except Exception as e:
        logging.error(f"Error extracting Spotify data: {e}")
        return None
    kwargs["ti"].xcom_push(key ='Spotify_data',value=spotify_data.to_json(orient='records'))
    return spotify_data.to_json(orient='records')


def transform_spotify(**kwargs):
    logging.info("Transforming Spotify data")
    ti = kwargs["ti"]
    logging.info(kwargs)

    str_data = ti.xcom_pull(task_ids="read_spotify", key='Spotify_data')
    
    if str_data is None:
        logging.error("No data to transform.")
        return None

    json_data = json.loads(str_data)
    transformer = TransformSpotify(pd.DataFrame(json_data))
    
    transformer.unnamed_to_id()
    transformer.drop_nan_records()
    transformer.normalize_data()
    transformer.filter_max_popularity_tracks()
    
    transformed_data = transformer.df.to_json(orient='records')
    logging.info(f"Transformed Spotify data: {transformer.df.head()}")
    return transformed_data


def extract_grammy(**kwargs):
    logging.info("Starting data extraction for Grammy")
    try:
        grammy_data = read_grammy_db()
        if grammy_data is None:
            logging.error("Failed to extract Grammy data.")
            return None
        logging.info("Grammy data extracted successfully.")
    except Exception as e:
        logging.error(f"Error extracting Grammy data: {e}")
        return None
    
    kwargs["ti"].xcom_push(key ='Grammy_data',value=grammy_data.to_json(orient='records'))
    return grammy_data.to_json(orient='records')


def transform_grammy(**kwargs):
    logging.info("Transforming Grammy data")
    ti = kwargs["ti"]
    logging.info(kwargs)

    str_data = ti.xcom_pull(task_ids="read_grammy", key='Grammy_data')
    
    if str_data is None:
        logging.error("No data to transform.")
        return None

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
    logging.info(f"Transformed Grammy data: {transformer.df.head()}")
    return transformed_data


def merge_data(**kwargs):
    logging.info("Starting merge process")
    ti = kwargs["ti"]
    
    str_data_grammy = ti.xcom_pull(task_ids="transform_grammy")
    str_data_spotify = ti.xcom_pull(task_ids="transform_spotify")

    if str_data_grammy is None or str_data_spotify is None:
        logging.error("No data to merge.")
        return None
    
    json_data_grammy = json.loads(str_data_grammy)
    json_data_spotify = json.loads(str_data_spotify)

    grammy_df = pd.json_normalize(data=json_data_grammy)
    spotify_df = pd.json_normalize(data=json_data_spotify)

    merge_data = MergeData(grammy_df, spotify_df)
    merged_df = merge_data.merge()
    logging.info(f"Merged data ready: {merged_df.head()}")
    kwargs["ti"].xcom_push(key ='Merged_data',value=merged_df.to_json(orient='records'))
    return merged_df.to_json(orient='records')

def load_data_to_db(**kwargs):
    logging.info("Starting load process")
    ti = kwargs["ti"]
    str_data = ti.xcom_pull(task_ids="merge")
    
    if str_data is None:
        logging.error("No data to load.")
        return None
    
    json_data = json.loads(str_data)
    data = pd.json_normalize(data=json_data)
    
    logging.info(f"Data to load is: {data}")
    logging.info("Loading data")

    try:
        loaded_data = load_data(data) 
        logging.info("Data loaded successfully into: merged_data")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
    
    kwargs["ti"].xcom_push(key ='Loaded_data',value=loaded_data.to_json(orient='records'))
    return loaded_data.to_json(orient='records')


def store_drive(**kwargs):
    logging.info("Starting store process")
    ti = kwargs["ti"]
    str_data = ti.xcom_pull(task_ids="load")
    
    if str_data is None:
        logging.error("No data to store.")
        return None
    
    json_data = json.loads(str_data)
    data = pd.json_normalize(data=json_data)
    
    logging.info(f"Data to store is: {data}")
    logging.info("Storing data")

    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')

    try:
        stored_data = upload_file(csv_bytes) 
        logging.info("Data stored successfully")
    except Exception as e:
        logging.error(f"Error storing data: {e}")
    
    kwargs["ti"].xcom_push(key ='Stored_data',value=stored_data.to_json(orient='records'))
    return stored_data.to_json(orient='records')

