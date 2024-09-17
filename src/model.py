'''
model.py

This module defines SQLAlchemy ORM models for representing candidates and their transformed data.

It includes:
    - `Candidates`: A model for storing raw candidate data.
    - `Candidates_transformed`: A model for storing transformed candidate data with an additional 'Hired' column.

Both models use SQLAlchemy's declarative base to define the structure of the tables and their attributes.

Imports:
- Column, Integer, String, Date from sqlalchemy: Used to define columns in the database tables.
- declarative_base from sqlalchemy.orm: Provides a base class for defining models.

Usage:
    These models can be used to interact with a database using SQLAlchemy, facilitating CRUD operations and data manipulation.
'''

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

base = declarative_base()

class Candidates(base):
    """
    SQLAlchemy model representing candidates.

    __tablename__ = 'Candidates'

    Attributes:
        ID (int): The unique identifier for each candidate (Primary Key, Auto Incremented).
        First_Name (str): The first name of the candidate.
        Last_Name (str): The last name of the candidate.
        Email (str): The email address of the candidate.
        Application_Date (date): The date when the candidate applied.
        Country (str): The country of the candidate.
        YOE (int): The years of experience of the candidate.
        Seniority (str): The seniority level of the candidate.
        Technology (str): The technology or field related to the candidate.
        Code_Challenge_Score (int): The score from the code challenge.
        Technical_Interview_Score (int): The score from the technical interview.

    Methods:
        __str__(self):
            Returns a string representation of the Candidate object, showing all attributes.
    """
    __tablename__ = 'Candidates'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(100), nullable=False)
    Last_Name = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False)
    Application_Date = Column(Date, nullable=False)
    Country = Column(String(100), nullable=False)
    YOE = Column(Integer, nullable=False)  # Years of Experience
    Seniority = Column(String(100), nullable=False)
    Technology = Column(String(100), nullable=False)
    Code_Challenge_Score = Column(Integer, nullable=False)
    Technical_Interview_Score = Column(Integer, nullable=False)

    def __str__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Candidate({attributes})"

class Candidates_transformed(base):
    """
    SQLAlchemy model representing transformed candidates data.

    __tablename__ = 'Candidates_transformed'

    Attributes:
        ID (int): The unique identifier for each candidate (Primary Key, Auto Incremented).
        First_Name (str): The first name of the candidate.
        Last_Name (str): The last name of the candidate.
        Email (str): The email address of the candidate.
        Application_Date (date): The date when the candidate applied.
        Country (str): The country of the candidate.
        YOE (int): The years of experience of the candidate.
        Seniority (str): The seniority level of the candidate.
        Technology (str): The technology or field related to the candidate.
        Code_Challenge_Score (int): The score from the code challenge.
        Technical_Interview_Score (int): The score from the technical interview.
        Hired (int): A flag indicating if the candidate was hired (1 for hired, 0 for not hired).

    Methods:
        __str__(self):
            Returns a string representation of the Candidate object, showing all attributes.
    """

    __tablename__ = 'Candidates_transformed'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(100), nullable=False)
    Last_Name = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False)
    Application_Date = Column(Date, nullable=False)
    Country = Column(String(100), nullable=False)
    YOE = Column(Integer, nullable=False)  # Years of Experience
    Seniority = Column(String(100), nullable=False)
    Technology = Column(String(100), nullable=False)
    Code_Challenge_Score = Column(Integer, nullable=False)
    Technical_Interview_Score = Column(Integer, nullable=False)
    Hired = Column(Integer, nullable=False)

    def __str__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Candidate({attributes})"