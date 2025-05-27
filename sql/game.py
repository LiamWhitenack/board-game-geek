from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from other_classes.item import Item
from other_classes.link import Link
from sql import Base
from sql.accessory import Accessory
from sql.artist import Artist
from sql.artist_game import ArtistGame
from sql.category import Category
from sql.category_game import CategoryGame
from sql.compilation import Compilation
from sql.designer_game import DesignerGame
from sql.expansion import Expansion
from sql.family import Family
from sql.family_game import FamilyGame
from sql.implementation import Implementation
from sql.mechanic import Mechanic
from sql.publisher import Publisher
from sql.publisher_game import PublisherGame


class Game(Base):
    __tablename__ = "game"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, default=None)
    url: Mapped[str | None] = mapped_column(Text, default=None)
    thumbnail: Mapped[str | None] = mapped_column(Text, default=None)
    image: Mapped[str | None] = mapped_column(Text, default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    year_published: Mapped[int | None] = mapped_column(Integer, default=None)
    min_players: Mapped[int | None] = mapped_column(Integer, default=None)
    max_players: Mapped[int | None] = mapped_column(Integer, default=None)
    best_player_count: Mapped[str | None] = mapped_column(Text, default=None)
    language_dependence: Mapped[str | None] = mapped_column(Text, default=None)
    recommended_player_counts: Mapped[str | None] = mapped_column(Text, default=None)
    playing_time: Mapped[int | None] = mapped_column(Integer, default=None)
    min_play_time: Mapped[int | None] = mapped_column(Integer, default=None)
    max_play_time: Mapped[int | None] = mapped_column(Integer, default=None)
    min_age: Mapped[str | None] = mapped_column(Integer, default=None)

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
        foreign_keys=[Compilation.game_id],
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
    def from_item(cls, item: Item):

        return cls(
            id=int(item._id),
            name=item.name,
            url=item.url,
            thumbnail=item.thumbnail,
            image=item.image,
            description=item.description,
            year_published=item.yearpublished,
            min_players=item.min_players,
            max_players=item.max_players,
            best_player_count=item.best_player_count,
            recommended_player_counts=item.recommended_player_counts,
            language_dependence=item.language_dependence,
            playing_time=item.playing_time,
            min_play_time=item.min_play_time,
            max_play_time=item.max_play_time,
            min_age=item.min_age,
        )

    @classmethod
    def from_link(cls, link: Link):
        return cls(
            id=link._id,
            name=link._value,
        )

    def enrich(self, item: Item):
        self.thumbnail = item.thumbnail
        self.image = item.image
        self.description = item.description
        self.year_published = item.yearpublished  # type: ignore[assignment]
        self.min_players = item.min_players  # type: ignore[assignment]
        self.max_players = item.max_players  # type: ignore[assignment]
        self.best_player_count = item.best_player_count
        self.recommended_player_counts = item.recommended_player_counts
        self.language_dependence = item.language_dependence
        self.playing_time = item.playing_time  # type: ignore[assignment]
        self.min_play_time = item.min_play_time  # type: ignore[assignment]
        self.max_play_time = item.max_play_time  # type: ignore[assignment]
        self.min_age = item.min_age  # type: ignore[assignment]
