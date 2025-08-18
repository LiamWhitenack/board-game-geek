from __future__ import annotations

from sqlalchemy import Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from other_classes.item import Item
from other_classes.link import Link
from sql import Base
from sql.accessory import Accessory
from sql.compilation import Compilation
from sql.expansion import Expansion
from sql.implementation import Implementation


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
    min_age: Mapped[int | None] = mapped_column(Integer, default=None)

    # ratings/statistics
    usersrated: Mapped[int | None] = mapped_column(Integer, default=None)
    average: Mapped[float | None] = mapped_column(Float, default=None)
    bayesaverage: Mapped[float | None] = mapped_column(Float, default=None)
    stddev: Mapped[float | None] = mapped_column(Float, default=None)
    median: Mapped[float | None] = mapped_column(Float, default=None)
    owned: Mapped[int | None] = mapped_column(Integer, default=None)
    trading: Mapped[int | None] = mapped_column(Integer, default=None)
    wanting: Mapped[int | None] = mapped_column(Integer, default=None)
    wishing: Mapped[int | None] = mapped_column(Integer, default=None)
    numcomments: Mapped[int | None] = mapped_column(Integer, default=None)
    numweights: Mapped[int | None] = mapped_column(Integer, default=None)
    averageweight: Mapped[float | None] = mapped_column(Float, default=None)

    # rank subtype columns
    rank_all: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_abstract: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_childrens: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_customizable: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_family: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_party: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_strategy: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_thematic: Mapped[int | None] = mapped_column(Integer, default=None)
    rank_wargames: Mapped[int | None] = mapped_column(Integer, default=None)

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
            # ratings/statistics
            usersrated=item.usersrated,
            average=item.average,
            bayesaverage=item.bayesaverage,
            stddev=item.stddev,
            median=item.median,
            owned=item.owned,
            trading=item.trading,
            wanting=item.wanting,
            wishing=item.wishing,
            numcomments=item.numcomments,
            numweights=item.numweights,
            averageweight=item.averageweight,
            # rank subtype columns
            rank_all=item.rank_all,
            rank_abstract=item.rank_abstract,
            rank_childrens=item.rank_childrens,
            rank_customizable=item.rank_customizable,
            rank_family=item.rank_family,
            rank_party=item.rank_party,
            rank_strategy=item.rank_strategy,
            rank_thematic=item.rank_thematic,
            rank_wargames=item.rank_wargames,
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

        # ratings/statistics
        self.usersrated = item.usersrated
        self.average = item.average
        self.bayesaverage = item.bayesaverage
        self.stddev = item.stddev
        self.median = item.median
        self.owned = item.owned
        self.trading = item.trading
        self.wanting = item.wanting
        self.wishing = item.wishing
        self.numcomments = item.numcomments
        self.numweights = item.numweights
        self.averageweight = item.averageweight

        # rank subtype columns
        self.rank_all = item.rank_all
        self.rank_abstract = item.rank_abstract
        self.rank_childrens = item.rank_childrens
        self.rank_customizable = item.rank_customizable
        self.rank_family = item.rank_family
        self.rank_party = item.rank_party
        self.rank_strategy = item.rank_strategy
        self.rank_thematic = item.rank_thematic
        self.rank_wargames = item.rank_wargames
