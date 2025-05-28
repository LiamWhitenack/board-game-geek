from time import sleep

from fetch.get_from_api import get_from_bgg
from sql.game import Game
from sql.session import session

for i in range(1, 10_000):
    print(i)
    j = 20 * i
    at_least_one_added = False
    for base in get_from_bgg(range(j + 1, j + 21)):
        at_least_one_added = True
        session.merge(base)
    if not at_least_one_added:
        break
    session.commit()
    sleep(5)
