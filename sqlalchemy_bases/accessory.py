from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from other_classes.link import Link
from sqlalchemy_bases import Base


class Accessory(Base):
    __tablename__ = "accessory"
    accessory_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    original_id = Column(Integer, ForeignKey("game.id"))

    # Relationship to 'Game' via accessory_id FK
    accessory_game = relationship(
        "Game", foreign_keys=[accessory_id], back_populates="accessory_for"
    )

    # Relationship to 'Game' via original_id FK
    original_game = relationship(
        "Game", foreign_keys=[original_id], back_populates="accessories"
    )

    @classmethod
    def from_link(cls, link: Link):
        return cls(original_id=link.reference_id, accessory_id=link._id)
