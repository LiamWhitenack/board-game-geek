from dataclasses import dataclass
from typing import Self


@dataclass
class Link:
    _type: str
    _id: str
    _value: str

    @classmethod
    def from_json(cls, json: dict[str, str]) -> Self:
        return cls(json["@type"], json["@id"], json["@value"])
