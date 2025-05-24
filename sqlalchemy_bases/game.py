from __future__ import annotations

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base
from sqlalchemy_bases.accessory import Accessory
from sqlalchemy_bases.compilation import Compilation
from sqlalchemy_bases.expansion import Expansion
from sqlalchemy_bases.implementation import Implementation


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    thumbnail = Column(Text)
    image = Column(Text)
    description = Column(Text)
    year_published = Column(Integer)
    min_players = Column(Integer)
    max_players = Column(Integer)
    best_player_count = Column(Integer)
    language_dependence = Column(Text)
    recommended_player_counts = Column(Text)
    playing_time = Column(Integer)
    min_play_time = Column(Integer)
    max_play_time = Column(Integer)
    min_age = Column(Integer)
    expansion = Column(Integer)
    accessory = Column(Integer)
    name = Column(Text)

    # Relationships
    artists = relationship("Artist", secondary="artist_game", back_populates="games")
    categories = relationship(
        "Category", secondary="category_game", back_populates="games"
    )
    families = relationship("Family", secondary="family_game", back_populates="games")
    publishers = relationship(
        "Publisher", secondary="publisher_game", back_populates="games"
    )

    accessory_for = relationship(
        "Accessory", foreign_keys=[Accessory.accessory_id], backref="accessory_game"
    )
    accessories = relationship(
        "Accessory", foreign_keys=[Accessory.original_id], backref="original_game"
    )

    expansions = relationship(
        "Expansion", foreign_keys=[Expansion.original_id], backref="base_game"
    )
    expansion_of = relationship(
        "Expansion", foreign_keys=[Expansion.expansion_id], backref="expanding_game"
    )

    compilations = relationship(
        "Compilation",
        foreign_keys=[Compilation.compilation_id],
        backref="compilation_game",
    )
    part_of_compilation = relationship(
        "Compilation", foreign_keys=[Compilation.contained_id], backref="contained_game"
    )

    implementations = relationship(
        "Implementation",
        foreign_keys=[Implementation.original_id],
        backref="original_game",
    )
    implemented_as = relationship(
        "Implementation",
        foreign_keys=[Implementation.implementation_id],
        backref="implementation_game",
    )

    @classmethod
    def from_json(cls, item: dict) -> Game:
        def get_language_dependence(item: dict) -> str:
            votes: list[dict[str, str]] = item["poll"][2]["results"]["result"]
            return max(votes, key=lambda x: int(x["@numvotes"]))["@value"]

        return cls(
            id=int(item["@id"]),
            thumbnail=item.get("thumbnail", ""),
            image=item.get("image", ""),
            description=item.get("description", ""),
            year_published=int(item["yearpublished"]["@value"]),
            min_players=int(item["minplayers"]["@value"]),
            max_players=int(item["maxplayers"]["@value"]),
            best_player_count=item["poll-summary"]["result"][0]["@value"],
            language_dependence=get_language_dependence(item),
            recommended_player_counts=item["poll-summary"]["result"][1]["@value"],
            playing_time=int(item["playingtime"]["@value"]),
            min_play_time=int(item["minplaytime"]["@value"]),
            max_play_time=int(item["maxplaytime"]["@value"]),
            min_age=int(item["minage"]["@value"]),
            expansion=item["@type"] == "boardgameexpansion",
            name=item["name"][0]["@value"],
        )
