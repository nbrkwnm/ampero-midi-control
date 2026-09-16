from dataclasses import dataclass, field

from .song import Song

@dataclass
class Setlist:
    name: str
    songs: list[Song] = field(default_factory=list)