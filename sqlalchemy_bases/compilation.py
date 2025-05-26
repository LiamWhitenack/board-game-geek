from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sqlalchemy_bases import Base


class Compilation(Base):
    __tablename__ = "compilation"
    game_id = Column(Integer, ForeignKey("game.id"))
    contained_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(game_id=link.reference_id, contained_id=link._id)
