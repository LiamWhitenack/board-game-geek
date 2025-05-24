from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class Accessory(Base):
    __tablename__ = "accessory"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    accessory_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
