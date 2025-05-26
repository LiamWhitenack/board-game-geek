from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base


class Designer(Base):
    __tablename__ = "designer"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="designer_game", back_populates="designers")

    @classmethod
    def from_link(cls, link):
        return cls(id=link["@id"], value=link["@value"])
