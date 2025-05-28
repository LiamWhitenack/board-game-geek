from sqlalchemy import Column, ForeignKey, Integer

from other_classes.link import Link
from sql import Base


class PublisherGame(Base):
    __tablename__ = "publisher_game"
    publisher_id = Column(Integer, ForeignKey("publisher.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: Link):
        return cls(publisher_id=link._id, game_id=link.reference_id)
