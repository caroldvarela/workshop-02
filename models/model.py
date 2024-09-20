from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

base = declarative_base()

class GrammyAward(base):
    __tablename__ = 'grammy_awards'

    year = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    published_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    category = Column(String(100), nullable=False)
    nominee = Column(String(200), nullable=False)
    artist = Column(String(200), nullable=False)
    workers = Column(String(500), nullable=False)
    img = Column(String(500), nullable=False)
    winner = Column(Boolean, nullable=False)

    def __str__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Grammy({attributes})"