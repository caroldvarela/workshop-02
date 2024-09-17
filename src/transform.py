"""
This module provides the `Transform` class for transforming and cleaning data read from a CSV file.

Imports:
    - pandas as pd: Used for data manipulation and analysis.

Classes:
    - Transform: Provides methods for data transformation on a pandas DataFrame.

    Methods:
        - __init__(self, file):
            Initializes a new instance of Transform and loads the DataFrame from a CSV file.
        - rename_columns(self):
            Renames the columns of the DataFrame to match the SQLAlchemy model.
        - insert_ids(self):
            Adds an 'ID' column to the DataFrame with unique values for each row.
        - add_hired_column(self):
            Adds a 'Hired' column to the DataFrame, indicating whether the candidate was hired based on the scores.
        - technology_to_category(self):
            Assigns a category to each row of the DataFrame based on the specified technology.
Usage:
    This module is used to prepare and transform candidate data for further processing or analysis.
    The `Transform` class provides a series of methods to clean and structure data according to specific rules.
    
"""

import pandas as pd

class Transform:
    """
    A class for transforming data from a CSV file.

    Attributes:
        df (pandas.DataFrame): DataFrame containing the data read from the CSV file.

    Methods:
    __init__(self, file):
            Initializes a new instance of Transform and loads the DataFrame from a CSV file.
        rename_columns(self):
            Renames the columns of the DataFrame to match the SQLAlchemy model.
        insert_ids(self):
            Adds an 'ID' column to the DataFrame with unique values for each row.
        add_hired_column(self):
            Adds a 'Hired' column to the DataFrame, indicating whether the candidate was hired based on the scores.
        technology_to_category(self):
            Assigns a category to each row of the DataFrame based on the specified technology.
    """
    
    def __init__(self, file):
        """
        Initializes the Transform class by reading a CSV file into a DataFrame.

        Args:
            file (str): Path to the CSV file to be read.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
            pd.errors.ParserError: If there is an error parsing the file.
        """
        self.df = pd.read_csv(file, sep=';', encoding='utf-8')

    def rename_columns(self):
        """
        Renames columns in the DataFrame to match the SQLAlchemy model naming conventions.

        """
        self.df.rename(columns={
            'First Name': 'First_Name',
            'Last Name': 'Last_Name',
            'Application Date': 'Application_Date',
            'Code Challenge Score': 'Code_Challenge_Score',
            'Technical Interview Score': 'Technical_Interview_Score'
        }, inplace=True)

    def insert_ids(self):
        """
        Inserts an 'ID' column into the DataFrame.

        This method creates a new column 'ID' with integer values starting from 1 up to the length of the DataFrame.
        """
        self.df['ID'] = range(1, len(self.df) + 1)

    def add_hired_column(self):
        """
        Adds a 'Hired' column to the DataFrame based on score.

        This method creates a new column 'Hired' where the value is 1 if both 'Code_Challenge_Score' and 
        'Technical_Interview_Score' are greater than or equal to 7, otherwise 0.
        """
        self.df['Hired'] = ((self.df['Code_Challenge_Score'] >= 7) & (self.df['Technical_Interview_Score'] >= 7)).astype(int)

    def technology_to_category(self):
        """
        Maps technology names to their corresponding categories and adds a 'Category' column.
        If a technology is not found in the mapping, 'Unknown' is used as the default category.
        """
        technology_to_category = {
            'Development - CMS Backend': 'Development',
            'Development - CMS Frontend': 'Development',
            'Development - Backend': 'Development',
            'Adobe Experience Manager': 'Development',
            'Development - Frontend': 'Development',
            'Development - FullStack': 'Development',
            'Game Development': 'Development',
            'DevOps': 'Development',
            'Mulesoft': 'Development',
            'Business Intelligence': 'Data Management and Analytics',
            'Business Analytics / Project Management': 'Data Management and Analytics',
            'Data Engineer': 'Data Management and Analytics',
            'Database Administration': 'Data Management and Analytics',
            'QA Manual': 'Quality',
            'QA Automation': 'Quality',
            'Security': 'Security',
            'Security Compliance': 'Security',
            'System Administration': 'System Administration',
            'Design': 'Design',
            'Client Success': 'Customer Engagement',
            'Social Media Community Management': 'Customer Engagement',
            'Technical Writing': 'Documentation',
            'Sales': 'Sales',
            'Salesforce': 'Sales'
        }

        self.df['Technology'] = self.df['Technology'].map(technology_to_category).fillna('Unknown')