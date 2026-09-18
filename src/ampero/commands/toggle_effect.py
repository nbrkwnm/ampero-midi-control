from dataclasses import dataclass

from domain.models.effect import EffectType

@dataclass(frozen=True)
class ToggleEffect:
    effect: EffectType
    enabled: bool