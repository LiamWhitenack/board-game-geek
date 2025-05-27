from sqlalchemy import Column, ForeignKey, Integer

from sql import Base


class ArtistGame(Base):
    __tablename__ = "artist_game"
    artist_id = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
