from time import sleep

from fetch.get_from_api import get_from_bgg
from sql.game import Game
from sql.session import session

at_least_one_added = [True for _ in range(10)]
for i in range(1, 100_000):
    print(i)
    j = 20 * i
    add_one = False
    for base in get_from_bgg(range(j + 1, j + 21)):
        add_one = True
        session.merge(base)

    del at_least_one_added[0]
    at_least_one_added.append(add_one)
    if not any(at_least_one_added):
        break
    session.commit()
    sleep(2)
