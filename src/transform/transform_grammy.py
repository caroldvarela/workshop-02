import pandas as pd

class TransformGrammy:

    def __init__(self, df):
        self.df = df
    
    def insert_ids(self):
        """
        Inserts an 'ID' column into the DataFrame.

        This method creates a new column 'ID' with integer values starting from 1 up to the length of the DataFrame.
        """
        self.df['ID'] = range(1, len(self.df) + 1)
    
    def remove_unwanted_grammmy_columns(self):
        self.df.drop(columns=['published_at', 'updated_at'])

    def remove_na_nominees(self):
        self.df = self.df.dropna(subset=['nominee'])

    def extract_artists(self):
        extracted_artists = self.df['workers'].str.extract(r'\(([^)]+)\)', expand=False)
        self.df['artist'] = self.df['artist'].fillna(extracted_artists)
    
    def remove_parentheses_from_artists(self):
        self.df['artist'] = self.df['artist'].str.replace(r'\(|\)', '', regex=True)
    
    def mark_winners(self):
        grouped = self.df.groupby(['year', 'title', 'category'])
        for name, group in grouped:
            if len(group) > 2:
                self.df.loc[group.index[0], 'winner'] = True
                self.df.loc[group.index[1:], 'winner'] = False

    def filter_winners(self):
        self.df = self.df[self.df['winner'] == True] #
    

    