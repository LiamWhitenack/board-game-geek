from dataclasses import dataclass
from typing import Any, Literal, Self

from other_classes.link import Link


@dataclass
class Item:
    _type: str
    _id: str
    name: str
    description: str
    yearpublished: int
    links: list[Link]
    thumbnail: str | None = None
    image: str | None = None
    min_players: int | None = None
    max_players: int | None = None
    best_player_count: str | None = None
    recommended_player_counts: str | None = None
    language_dependence: str | None = None
    playing_time: int | None = None
    min_play_time: int | None = None
    max_play_time: int | None = None
    min_age: int | None = None

    @classmethod
    def from_json(cls, json: dict[str, Any] | Literal["error"]) -> Self | None:
        if json == "error":
            return None
        try:
            id = json["@id"]
            best_player_count, recommended_player_counts = cls.extract_poll_summary(
                json.get("poll-summary")
            )
            primary_name: dict = (
                json["name"] if isinstance(json["name"], dict) else json["name"][0]
            )
            links = list(
                filter(
                    lambda link: link is not None,
                    [Link.from_json(link, id) for link in json.get("link", [])],
                )
            )
            return cls(
                _type=json["@type"],
                _id=id,
                thumbnail=json.get("thumbnail"),
                image=json.get("image"),
                name=primary_name.get("@value", "Unknown"),
                description=json.get("description", ""),
                yearpublished=int(json.get("yearpublished", {}).get("@value", 0)),
                links=links,
                min_players=int(json.get("minplayers", {}).get("@value", 0)),
                max_players=int(json.get("maxplayers", {}).get("@value", 0)),
                best_player_count=best_player_count,
                recommended_player_counts=recommended_player_counts,
                language_dependence=cls.extract_language_dependence(json),
                playing_time=int(json.get("playingtime", {}).get("@value", 0)),
                min_play_time=int(json.get("minplaytime", {}).get("@value", 0)),
                max_play_time=int(json.get("maxplaytime", {}).get("@value", 0)),
                min_age=int(json.get("minage", {}).get("@value", 0)),
            )
        except KeyError:
            return None

    @staticmethod
    def extract_name(name: list[dict] | dict):
        if isinstance(name, list):
            name = name[0]
        return name["@value"]

    @staticmethod
    def extract_poll_summary(json):
        return json.get("result", [{}, {}])[0].get("@value"), json.get(
            "result", [{}, {}]
        )[1].get("@value")

    @staticmethod
    def extract_language_dependence(item: dict[str, list]):
        for poll in item.get("poll", []):
            if poll["@name"] == "language_dependence":
                results = poll["results"]["result"]
                top = max(results, key=lambda r: int(r.get("@numvotes", 0)))
                return top.get("@value")
        return None
