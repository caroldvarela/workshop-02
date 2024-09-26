import pandas as pd
from fuzzywuzzy import process

class MergeData:
    def __init__(self, grammy_df, spotify_df):
        self.df_grammy = grammy_df
        self.spotify_df = spotify_df

    def merge(self):
        self.df_grammy.rename(columns={
            'winner': 'grammy_winner',
            'year': 'grammy_year',
            'nominee': 'track_name',
            'artist': 'artists'
        }, inplace=True)

        df_aggregated = self.df_grammy.groupby(['track_name', 'artists']).agg({
            'grammy_winner': 'max',
            'grammy_year': 'max'
        }).reset_index()

        grammy_count = self.df_grammy.groupby(['track_name', 'artists']).size().reset_index(name='number_wins')

        self.df_grammy = pd.merge(df_aggregated, grammy_count, on=['track_name', 'artists'], how='left')

        # fuzzywuzzy
        def find_best_match(row):
            track_name = row['track_name']
            artist = row['artists']
            
            spotify_artists = self.spotify_df[self.spotify_df['track_name'] == track_name]['artists'].tolist()
            best_match = None
            best_score = 0

            for spotify_artist in spotify_artists:
                match, score = process.extractOne(artist, [spotify_artist])
                if score > best_score:
                    best_score = score
                    best_match = match
                if best_score >= 80:  
                    return best_match
            return None

        self.df_grammy['artists'] = self.df_grammy.apply(find_best_match, axis=1)

        merged_df = pd.merge(self.spotify_df, self.df_grammy, left_on=['track_name', 'artists'], right_on=['track_name', 'artists'], how='left')

        merged_df['grammy_winner'].fillna('False', inplace=True)
        merged_df['number_wins'].fillna(0, inplace=True)

        merged_df['grammy_year'] = merged_df['grammy_year'].astype('Int64')
        merged_df['number_wins'] = pd.to_numeric(merged_df['number_wins'], downcast='integer', errors='coerce')

        merged_df = merged_df.sort_values(by=['artists', 'track_name']).reset_index(drop=True)
        return merged_df