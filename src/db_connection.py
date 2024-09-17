"""
This module provides functionality to build a SQLAlchemy engine for connecting
to a PostgreSQL database using configuration values from environment variables.

It defines the following function:
- build_engine: Creates and returns a SQLAlchemy engine for the database.

Usage:
    This module is used to establish a connection to a PostgreSQL database by creating an engine
    with SQLAlchemy. The `build_engine` function retrieves connection details from environment variables
    and handles potential errors during the connection process.
    
"""

from decouple import config, UndefinedValueError
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def build_engine():
    """
    Creates a SQLAlchemy engine for connecting to the PostgreSQL database using
    configuration values from environment variables.

    Returns:
        sqlalchemy.engine.base.Engine: The SQLAlchemy engine connected to the database.

    Raises:
        UndefinedValueError: If any required environment variable is missing.
        SQLAlchemyError: If there is an error connecting to the database.
    """
    try:
        dialect = config('PGDIALECT')
        user = config('PGUSER')
        passwd = config('PGPASSWD')
        host = config('PGHOST')
        port = config('PGPORT')
        db = config('PGDB')
    except UndefinedValueError as e:
        print(f"Missing environment variable: {e}")
        raise

    database_url = (f"{dialect}://{user}:{passwd}@{host}:{port}/{db}")

    # Test the connection
    try:
        engine = create_engine(database_url)
        print(f"Successfully connected to the database {db}!")
        return engine
    except SQLAlchemyError as e:
        print(f"Failed to connect to the database: {e}")


