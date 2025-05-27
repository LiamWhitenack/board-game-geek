from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from other_classes.link import Link
from sql import Base


class Family(Base):
    __tablename__ = "family"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="family_game", back_populates="families")

    @classmethod
    def from_link(cls, link: Link):
        return cls(id=link._id, value=link._value)
