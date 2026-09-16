from dataclasses import dataclass

@dataclass(frozen=True)
class Preset:
    number: int
    name: str = ""