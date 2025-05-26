from __future__ import annotations

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from sqlalchemy_bases import Base
from sqlalchemy_bases.accessory import Accessory
from sqlalchemy_bases.artist import Artist
from sqlalchemy_bases.artist_game import ArtistGame
from sqlalchemy_bases.category import Category
from sqlalchemy_bases.category_game import CategoryGame
from sqlalchemy_bases.compilation import Compilation
from sqlalchemy_bases.designer_game import DesignerGame
from sqlalchemy_bases.expansion import Expansion
from sqlalchemy_bases.family import Family
from sqlalchemy_bases.family_game import FamilyGame
from sqlalchemy_bases.implementation import Implementation
from sqlalchemy_bases.mechanic import Mechanic
from sqlalchemy_bases.publisher import Publisher
from sqlalchemy_bases.publisher_game import PublisherGame


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
    name = Column(Text)

    # Relationships
    artists = relationship("Artist", secondary="artist_game", back_populates="games")
    designers = relationship(
        "Designer", secondary="designer_game", back_populates="games"
    )
    categories = relationship(
        "Category", secondary="category_game", back_populates="games"
    )
    families = relationship("Family", secondary="family_game", back_populates="games")
    publishers = relationship(
        "Publisher", secondary="publisher_game", back_populates="games"
    )

    accessory_for = relationship(
        "Accessory",
        foreign_keys=[Accessory.accessory_id],
        back_populates="accessory_game",
    )
    accessories = relationship(
        "Accessory",
        foreign_keys=[Accessory.original_id],
        back_populates="original_game",
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
    def from_json(cls, item):
        def extract_name(name: list[dict] | dict):
            if isinstance(name, list):
                return extract_name(name[0])
            return name["@value"]

        def extract_poll_summary(poll):
            best = None
            recommended = None
            for entry in poll.get("poll-summary", {}).get("result", []):
                if entry["@name"] == "bestwith":
                    best = entry["@value"]
                elif entry["@name"] == "recommmendedwith":
                    recommended = entry["@value"]
            return best, recommended

        best_count, recommended_counts = extract_poll_summary(item)

        return cls(
            id=int(item["@id"]),
            thumbnail=item.get("thumbnail"),
            image=item.get("image"),
            name=extract_name(item.get("name", [])),
            description=item.get("description"),
            year_published=int(item.get("yearpublished", {}).get("@value", 0)),
            min_players=int(item.get("minplayers", {}).get("@value", 0)),
            max_players=int(item.get("maxplayers", {}).get("@value", 0)),
            best_player_count=best_count,
            recommended_player_counts=recommended_counts,
            language_dependence=cls.extract_language_dependence(item),
            playing_time=int(item.get("playingtime", {}).get("@value", 0)),
            min_play_time=int(item.get("minplaytime", {}).get("@value", 0)),
            max_play_time=int(item.get("maxplaytime", {}).get("@value", 0)),
            min_age=int(item.get("minage", {}).get("@value", 0)),
        )

    @staticmethod
    def extract_language_dependence(item):
        for poll in item.get("poll", []):
            if poll["@name"] == "language_dependence":
                results = poll["results"]["result"]
                top = max(results, key=lambda r: int(r.get("@numvotes", 0)))
                return top.get("@value")
        return None
