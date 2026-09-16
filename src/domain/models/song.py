from dataclasses import dataclass, field

from .scene import Scene

@dataclass
class Song:
    name: str
    scenes: list[Scene] = field(default_factory=list)