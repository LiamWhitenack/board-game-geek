from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql import Base
from sql.accessory import Accessory
from sql.artist import Artist
from sql.artist_game import ArtistGame
from sql.category import Category
from sql.category_game import CategoryGame
from sql.compilation import Compilation
from sql.expansion import Expansion
from sql.family import Family
from sql.family_game import FamilyGame
from sql.game import Game
from sql.implementation import Implementation
from sql.mechanic import Mechanic
from sql.publisher import Publisher
from sql.publisher_game import PublisherGame

# Replace 'your_database.db' with your actual database file name
DATABASE_URL = "postgresql+psycopg2://lwhitenack:testpword@localhost:5432/bgg-db"
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()
