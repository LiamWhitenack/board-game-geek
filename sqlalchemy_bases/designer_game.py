from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class DesignerGame(Base):
    __tablename__ = "designer_game"
    designer_id = Column(Integer, ForeignKey("designer.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
