from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class CategoryGame(Base):
    __tablename__ = "category_game"
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(category_id=link._id, game_id=link.reference_id)
