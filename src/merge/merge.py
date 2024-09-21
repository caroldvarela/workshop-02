import pandas as pd

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


        self.df_grammy['artists_trimmed'] = self.df_grammy['artists'].str[:9]
        self.df_grammy['artists'] = None

        for index, row in self.df_grammy.iterrows():
            track_name = row['track_name']
            trimmed_artist = row['artists_trimmed']
            if pd.notnull(trimmed_artist):
                spotify_match = self.spotify_df[self.spotify_df['track_name'] == track_name]
                if not spotify_match.empty:
                    if spotify_match['artists'].str.contains(trimmed_artist, na=False).any():
                        self.df_grammy.at[index, 'artists'] = spotify_match.loc[
                            spotify_match['artists'].str.contains(trimmed_artist, na=False), 'artists'].values[0]

        merged_df = pd.merge(self.spotify_df, self.df_grammy, on=['track_name', 'artists'], how='left')
        merged_df.drop(columns=['artists_trimmed'], inplace=True)
        merged_df['grammy_winner'].fillna('False', inplace=True)
        merged_df['number_wins'].fillna(0, inplace=True)
        merged_df['grammy_year'] = merged_df['grammy_year'].astype('Int64')
        merged_df['number_wins'] = pd.to_numeric(merged_df['number_wins'], downcast='integer', errors='coerce')
        
        return merged_df