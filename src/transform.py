import pandas as pd

class Transform:

    def __init__(self, file):
        self.df = pd.read_csv(file, sep=';', encoding='utf-8')

    def insert_ids(self):
        """
        Inserts an 'ID' column into the DataFrame.

        This method creates a new column 'ID' with integer values starting from 1 up to the length of the DataFrame.
        """
        self.df['ID'] = range(1, len(self.df) + 1)
    
    def unnamed_to_id(self):
        self.df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    
    def drop_nan_records(self):
        nan_record_index = self.df[self.df.isna().any(axis=1)].index
        self.df.drop(nan_record_index, inplace=True)

    def normalize_data(self):
        for col in self.df.select_dtypes(include=['object']):
            self.df[col] = self.df[col].str.title().str.strip()
    
    def filter_max_popularity_tracks(self):
        df_max_popularity = self.df.loc[self.df.groupby(['track_name', 'artists'])['popularity'].idxmax()].reset_index(drop=True)
        track_ids_to_keep = df_max_popularity[['track_name', 'artists', 'track_id']].drop_duplicates()
        self.df = self.df.merge(track_ids_to_keep, on=['track_name', 'artists', 'track_id'])

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
    
    
    
