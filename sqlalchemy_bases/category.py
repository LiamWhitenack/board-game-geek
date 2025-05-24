from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="category_game", back_populates="categories")

    @classmethod
    def from_link(cls, link):
        return cls(id=link["@id"], value=link["@value"])
