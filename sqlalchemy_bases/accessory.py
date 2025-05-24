from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class Accessory(Base):
    __tablename__ = "accessory"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    accessory_id = Column(Integer, primary_key=True)

    @classmethod
    def from_link(cls, link):
        return cls(id=link["@id"], value=link["@value"])
