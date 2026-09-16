from dataclasses import dataclass, field

from .effect import Effect
from .preset import Preset

@dataclass
class Scene:
    name: str
    preset: Preset | None = None
    effects: list[Effect] = field(default_factory=list)