from sqlalchemy import Column, Integer,Float, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

base = declarative_base()

class GrammyAward(base):
    __tablename__ = 'grammy_awards'

    ID = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    nominee = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    workers = Column(String, nullable=True)
    img = Column(String, nullable=True)
    winner = Column(Boolean, nullable=False)

    def __str__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Grammy({attributes})"

class MergedDAta(base):
    __tablename__ = 'merged_data'

    ID = Column(Integer, primary_key=True)
    track_id = Column(String, nullable=False) 
    artists = Column(String, nullable=False)
    album_name = Column(String, nullable=False)
    track_name = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    explicit = Column(Boolean, nullable=False)
    danceability = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    key = Column(Integer, nullable=False)
    loudness = Column(Float, nullable=False)
    mode = Column(Integer, nullable=False)
    speechiness = Column(Float, nullable=False)
    acousticness = Column(Float, nullable=False)
    instrumentalness = Column(Float, nullable=False)
    liveness = Column(Float, nullable=False)
    valence = Column(Float, nullable=False)
    tempo = Column(Float, nullable=False)
    time_signature = Column(Integer, nullable=False)
    track_genre = Column(String, nullable=True)
    grammy_winner = Column(Boolean, nullable=False, default=False)
    grammy_year = Column(Integer, nullable=True)
    number_wins = Column(Integer, nullable=True, default=0)

    def __str__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Grammy({attributes})"