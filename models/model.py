from sqlalchemy import Column, Integer, String, DateTime, Boolean
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