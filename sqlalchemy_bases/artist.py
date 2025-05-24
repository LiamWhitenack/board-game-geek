from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base


class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="artist_game", back_populates="artists")

    @classmethod
    def from_link(cls, link):
        return cls(id=link["@id"], value=link["@value"])
