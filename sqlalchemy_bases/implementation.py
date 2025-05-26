from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sqlalchemy_bases import Base


class Implementation(Base):
    __tablename__ = "implementation"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    implementation_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(original_id=link.reference_id, implementation_id=link._id)
