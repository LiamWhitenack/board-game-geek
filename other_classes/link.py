from dataclasses import dataclass
from typing import Self


@dataclass
class Link:
    _type: str
    _id: str
    _value: str
    reference_id: str

    @classmethod
    def from_json(cls, json: dict[str, str], reference_id: str) -> Self | None:
        try:
            return cls(json["@type"], json["@id"], json["@value"], reference_id)
        except KeyError:
            return None
