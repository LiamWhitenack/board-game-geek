from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class CategoryGame(Base):
    __tablename__ = "category_game"
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
