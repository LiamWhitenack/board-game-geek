from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class DesignerGame(Base):
    __tablename__ = "designer_game"
    designer_id = Column(Integer, ForeignKey("designer.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(designer_id=link._id, game_id=link.reference_id)
