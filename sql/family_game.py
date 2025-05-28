from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class FamilyGame(Base):
    __tablename__ = "family_game"
    family_id = Column(Integer, ForeignKey("family.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(family_id=link._id, game_id=link.reference_id)
