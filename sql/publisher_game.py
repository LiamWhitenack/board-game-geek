from sqlalchemy import Column, ForeignKey, Integer

from sql import Base


class PublisherGame(Base):
    __tablename__ = "publisher_game"
    publisher_id = Column(Integer, ForeignKey("publisher.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
