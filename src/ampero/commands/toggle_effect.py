from dataclasses import dataclass

@dataclass(frozen=True)
class ToggleEffect:
    effect: str
    enabled: bool

    def __post_init__(self) -> None:
        if not self.effect:
            raise ValueError(
                "Effect must not be empty."
            )