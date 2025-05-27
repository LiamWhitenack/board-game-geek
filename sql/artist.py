from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from other_classes.link import Link
from sql import Base


class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="artist_game", back_populates="artists")

    @classmethod
    def from_link(cls, link: Link):
        return cls(id=link._id, value=link._value)
