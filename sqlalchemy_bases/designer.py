from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from other_classes.link import Link
from sqlalchemy_bases import Base


class Designer(Base):
    __tablename__ = "designer"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="designer_game", back_populates="designers")

    @classmethod
    def from_link(cls, link: Link):
        return cls(id=link._id, value=link._value)
