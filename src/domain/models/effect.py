from dataclasses import dataclass
from enum import Enum

class EffectType(Enum):
    FX1 = "fx1"
    FX2 = "fx2"
    FX3 = "fx3"
    DELAY = "delay"
    REVERB = "reverb"

@dataclass
class Effect:
    type: EffectType
    enabled: bool = False