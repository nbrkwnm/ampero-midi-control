from dataclasses import dataclass

from ..models.preset import Preset

@dataclass
class AmperoState:
    preset: Preset | None = None