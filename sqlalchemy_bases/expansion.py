from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class Expansion(Base):
    __tablename__ = "expansion"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    expansion_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
