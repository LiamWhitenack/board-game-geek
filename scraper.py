from api_calls import (
    GAME_SKELETONS,
    LINK_MAP,
    MAKE_A_NEW_GAME,
    SEEN_LINKS,
    fetch_things,
)
from other_classes.item import Item
from session_engine import session
from sqlalchemy_bases import Base
from sqlalchemy_bases.game import Game

seen_games: set[str] = set()
for item in map(Item.from_json, fetch_things(range(1, 21))):
    session.merge(Game.from_item(item))
    for link in item.links:
        if link._id in SEEN_LINKS.get(link._type, set()):
            continue
        if (base := LINK_MAP.get(link._type)) is not None:
            if link._type in MAKE_A_NEW_GAME:
                if link._id not in seen_games:
                    session.add(Game.from_link(link))
                    seen_games.add(link._id)
            SEEN_LINKS.get(link._type, set()).add(link._id)
            session.add(base.from_link(link))

    session.commit()
session.query(Game)
