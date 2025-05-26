import time
from collections.abc import Iterable

import requests
from xmltodict import parse

from sqlalchemy_bases.accessory import Accessory
from sqlalchemy_bases.artist import Artist
from sqlalchemy_bases.category import Category
from sqlalchemy_bases.designer import Designer
from sqlalchemy_bases.expansion import Expansion
from sqlalchemy_bases.family import Family
from sqlalchemy_bases.implementation import Implementation
from sqlalchemy_bases.mechanic import Mechanic
from sqlalchemy_bases.publisher import Publisher


def fetch_things(
    ids: Iterable[int], max_retries: int = 5, retries: int = 0
) -> list[dict]:
    url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={','.join(map(str, ids))}"
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return parse(response.text)["items"].get("item", None)  # type: ignore[index]
        elif response.status_code == 202:
            print("BGG says: not ready yet (202). Waiting...")
            time.sleep(5)
            retries += 1
            return fetch_things(ids, max_retries, retries)
        else:
            print(f"Unexpected status: {response.status_code}")
            break
    raise Exception()


LINK_MAP = dict(
    boardgamecategory=Category,
    boardgamemechanic=Mechanic,
    boardgamefamily=Family,
    boardgameaccessory=Accessory,
    boardgameartist=Artist,
    boardgamedesigner=Designer,
    boardgamepublisher=Publisher,
    # boardgameimplementation=Implementation,
    # boardgameexpansion=Expansion,
)

SEEN_LINKS: dict[str, set] = {k: set() for k in LINK_MAP}
