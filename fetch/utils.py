from sql.accessory import Accessory
from sql.artist import Artist
from sql.category import Category
from sql.designer import Designer
from sql.expansion import Expansion
from sql.family import Family
from sql.implementation import Implementation
from sql.mechanic import Mechanic
from sql.publisher import Publisher

LINK_MAP = dict(
    boardgamecategory=Category,
    boardgamemechanic=Mechanic,
    boardgamefamily=Family,
    boardgameaccessory=Accessory,
    boardgameartist=Artist,
    boardgamedesigner=Designer,
    boardgamepublisher=Publisher,
    boardgameimplementation=Implementation,
    boardgameexpansion=Expansion,
)
MAKE_A_NEW_GAME = {
    "boardgameaccessory",
    "boardgameimplementation",
    "boardgameexpansion",
    "boardgameexpansion",
    "boardgameexpansion",
}
