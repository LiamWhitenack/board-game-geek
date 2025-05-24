from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base


class Family(Base):
    __tablename__ = "family"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    games = relationship("Game", secondary="family_game", back_populates="families")
