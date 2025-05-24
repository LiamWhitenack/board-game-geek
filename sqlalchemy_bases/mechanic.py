from sqlalchemy import Column, Integer, Text

from sqlalchemy_bases import Base


class Mechanic(Base):
    __tablename__ = "mechanic"
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    @classmethod
    def from_link(cls, link):
        return cls(id=link["@id"], value=link["@value"])
