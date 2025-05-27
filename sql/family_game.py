from sqlalchemy import Column, ForeignKey, Integer

from sql import Base


class FamilyGame(Base):
    __tablename__ = "family_game"
    family_id = Column(Integer, ForeignKey("family.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
