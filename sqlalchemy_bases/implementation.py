from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy_bases import Base


class Implementation(Base):
    __tablename__ = "implementation"
    original_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
    implementation_id = Column(Integer, ForeignKey("game.id"), primary_key=True)

    @classmethod
    def from_link(cls, link: dict):
        return cls(original_id=link["@reference_id"], implementation_id=link["@id"])
