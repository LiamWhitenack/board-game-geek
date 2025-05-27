import time
from collections.abc import Iterable

import requests
from xmltodict import parse

from fetch.seen import SEEN_GAMES, SEEN_LINKS
from fetch.utils import LINK_MAP, MAKE_A_NEW_GAME
from other_classes.item import Item
from sql import Base
from sql.game import Game


def fetch_things(
    ids: Iterable[int], max_retries: int = 5, retries: int = 0
) -> list[dict]:
    url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={','.join(map(str, ids))}"
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return parse(response.text)["items"].get("item", [])  # type: ignore[index]
        elif response.status_code == 202:
            print("BGG says: not ready yet (202). Waiting...")
            time.sleep(5)
            retries += 1
            return fetch_things(ids, max_retries, retries)
        else:
            print(f"Unexpected status: {response.status_code}")
            break
    raise Exception()


def get_from_bgg(things: Iterable[int]) -> Iterable[Base]:
    for item in map(Item.from_json, fetch_things(things)):
        if item is None:
            continue
        SEEN_GAMES.add(item._id)
        yield (Game.from_item(item))
        for link in item.links:
            if link._id in SEEN_LINKS.get(link._type, set()):
                continue
            if (base := LINK_MAP.get(link._type)) is not None:
                if link._type in MAKE_A_NEW_GAME:
                    if link._id not in SEEN_GAMES:
                        yield (Game.from_link(link))
                        SEEN_GAMES.add(link._id)
                if link._id not in (seen_links := SEEN_LINKS.get(link._type, set())):
                    seen_links.add(link._id)
                    yield (base.from_link(link))  # type: ignore[attr-defined]
