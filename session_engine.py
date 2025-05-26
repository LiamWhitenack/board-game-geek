from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_bases import Base
from sqlalchemy_bases.accessory import Accessory
from sqlalchemy_bases.artist import Artist
from sqlalchemy_bases.artist_game import ArtistGame
from sqlalchemy_bases.category import Category
from sqlalchemy_bases.category_game import CategoryGame
from sqlalchemy_bases.compilation import Compilation
from sqlalchemy_bases.expansion import Expansion
from sqlalchemy_bases.family import Family
from sqlalchemy_bases.family_game import FamilyGame
from sqlalchemy_bases.game import Game
from sqlalchemy_bases.implementation import Implementation
from sqlalchemy_bases.mechanic import Mechanic
from sqlalchemy_bases.publisher import Publisher
from sqlalchemy_bases.publisher_game import PublisherGame

# Replace 'your_database.db' with your actual database file name
engine = create_engine("sqlite:///:memory:", echo=True)

Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()
