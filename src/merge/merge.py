import pandas as pd
from fuzzywuzzy import process

class MergeData:
    def __init__(self, grammy_df, spotify_df):
        # Initialize the class with Grammy and Spotify dataframes
        self.df_grammy = grammy_df
        self.spotify_df = spotify_df

    def merge(self):
        # Rename columns in the Grammy dataframe for clarity
        self.df_grammy.rename(columns={
            'winner': 'grammy_winner',
            'year': 'grammy_year',
            'nominee': 'track_name',
            'artist': 'artists'
        }, inplace=True)

        # Aggregate Grammy data by track and artist to get grammy_winner and year
        df_aggregated = self.df_grammy.groupby(['track_name', 'artists']).agg({
            'grammy_winner': 'max',
            'grammy_year': 'max'
        }).reset_index()

         # Count the number of Grammy wins for each track and artist
        grammy_count = self.df_grammy.groupby(['track_name', 'artists']).size().reset_index(name='number_wins')

        # Merge the aggregated Grammy data with the count of wins
        self.df_grammy = pd.merge(df_aggregated, grammy_count, on=['track_name', 'artists'], how='left')

        # Define a function to find the best matching artist using fuzzy matching
        def find_best_match(row):
            track_name = row['track_name']
            artist = row['artists']
            
            # Get the list of artists from the Spotify dataframe that match the track name
            spotify_artists = self.spotify_df[self.spotify_df['track_name'] == track_name]['artists'].tolist()
            best_match = None
            best_score = 0

            # Iterate through Spotify artists to find the best match
            for spotify_artist in spotify_artists:
                match, score = process.extractOne(artist, [spotify_artist])
                if score > best_score:
                    best_score = score
                    best_match = match
                # If a good match is found, return it
                if best_score >= 80:  
                    return best_match
            return None

        # Apply the best match function to each row in the Grammy dataframe
        self.df_grammy['artists'] = self.df_grammy.apply(find_best_match, axis=1)

        # Merge the Grammy dataframe with the Spotify dataframe based on track name and artist
        merged_df = pd.merge(self.spotify_df, self.df_grammy, left_on=['track_name', 'artists'], right_on=['track_name', 'artists'], how='left')

        # Fill missing Grammy winner information and count of win
        merged_df['grammy_winner'].fillna('False', inplace=True)
        merged_df['number_wins'].fillna(0, inplace=True)

        # Convert 'grammy_year' to nullable integer type and 'number_wins' to numeric
        merged_df['grammy_year'] = merged_df['grammy_year'].astype('Int64')
        merged_df['number_wins'] = pd.to_numeric(merged_df['number_wins'], downcast='integer', errors='coerce')

        # Sort the merged dataframe by artist and track name, resetting the index
        merged_df = merged_df.sort_values(by=['artists', 'track_name']).reset_index(drop=True)
        return merged_df