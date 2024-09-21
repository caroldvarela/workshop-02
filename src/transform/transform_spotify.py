import pandas as pd

class TransformSpotify:

    def __init__(self, file):
        self.df = pd.read_csv(file, sep=';', encoding='utf-8')

    def unnamed_to_id(self):
            self.df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    
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
