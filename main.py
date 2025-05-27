from fetch.get_from_api import get_from_bgg
from sql.game import Game
from sql.session import session

for i in range(100):
    j = 20 * i
    for base in get_from_bgg(range(j + 1, j + 21)):
        session.merge(base)
        session.commit()
session.query(Game).all()
