from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class Compilation(Base):
    __tablename__ = "compilation"
    compilation_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    contained_id = Column(Integer, ForeignKey("game.id"))
