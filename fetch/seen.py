from fetch.utils import LINK_MAP

SEEN_GAMES: set[str] = set()
SEEN_LINKS: dict[str, set] = {k: set() for k in LINK_MAP}
