from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class Expansion(Base):
    __tablename__ = "expansion"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    expansion_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(original_id=link.reference_id, expansion_id=link._id)
