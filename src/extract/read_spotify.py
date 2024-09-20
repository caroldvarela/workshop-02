import pandas as pd

def read_spotify_csv():
    try:
        df = pd.read_csv('../data/spotify_dataset.csv', sep=',', encoding='utf-8')
        return df
    except Exception as e:
        return None