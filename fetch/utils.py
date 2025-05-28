from sql.accessory import Accessory
from sql.artist import Artist
from sql.artist_game import ArtistGame
from sql.category import Category
from sql.category_game import CategoryGame
from sql.designer import Designer
from sql.designer_game import DesignerGame
from sql.expansion import Expansion
from sql.family import Family
from sql.family_game import FamilyGame
from sql.implementation import Implementation
from sql.mechanic import Mechanic
from sql.publisher import Publisher
from sql.publisher_game import PublisherGame

LINK_MAP = dict(
    boardgamecategory=Category,
    boardgamemechanic=Mechanic,
    boardgameaccessory=Accessory,
    boardgameartist=Artist,
    boardgamedesigner=Designer,
    boardgamefamily=Family,
    boardgamepublisher=Publisher,
    boardgameimplementation=Implementation,
    boardgameexpansion=Expansion,
)
ASSOCIATION_MAP = dict(
    boardgamecategory=CategoryGame,
    boardgameartist=ArtistGame,
    boardgamedesigner=DesignerGame,
    boardgamefamily=FamilyGame,
    boardgamepublisher=PublisherGame,
)
MAKE_A_NEW_GAME = {
    "boardgameaccessory",
    "boardgameimplementation",
    "boardgameexpansion",
    "boardgameexpansion",
    "boardgameexpansion",
}
