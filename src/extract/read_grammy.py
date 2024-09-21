import sys 
import os
from dotenv import load_dotenv
import pandas as pd
from db.db_connection import build_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from models.model import GrammyAward
from sqlalchemy.exc import SQLAlchemyError
from src.transform.transform_grammy import TransformGrammy

load_dotenv()
work_dir = os.getenv('WORK_DIR')

sys.path.append(work_dir)


def read_grammy_db():
    engine = build_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        inspector = inspect(engine)

        if inspector.has_table('grammy_awards'):
            try:
                GrammyAward.__table__.drop(engine)
            except SQLAlchemyError as e:
                print(f"Error dropping table: {e}")
                raise

        try:
            GrammyAward.__table__.create(engine)
            print("Table creation was successful.")
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")
            raise

    except SQLAlchemyError as error:
        print(f"An error occurred: {error}")
        return None

    try:

        df = pd.read_csv('./data/the_grammy_awards.csv', sep=',', encoding='utf-8')
        transformer = TransformGrammy(df)
        transformer.insert_ids()
        with engine.connect() as connection:
            transformer.df.to_sql('grammy_awards', con=connection, if_exists='append', index=False)
        return transformer.df


    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        if session:
            session.close()