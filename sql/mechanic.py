from sqlalchemy import Column, Integer, Text

from other_classes.link import Link
from sql import Base


class Mechanic(Base):
    __tablename__ = "mechanic"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    @classmethod
    def from_link(cls, link: Link):
        return cls(id=link._id, value=link._value)
