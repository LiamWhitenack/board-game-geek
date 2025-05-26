from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from other_classes.link import Link
from sqlalchemy_bases import Base


class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship(
        "Game", secondary="publisher_game", back_populates="publishers"
    )

    @classmethod
    def from_link(cls, link: Link):
        return cls(id=link._id, value=link._value)
