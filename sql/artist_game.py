from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class ArtistGame(Base):
    __tablename__ = "artist_game"
    artist_id = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(artist_id=link._id, game_id=link.reference_id)
