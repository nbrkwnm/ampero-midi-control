from dataclasses import dataclass

@dataclass(frozen=True)
class SelectPreset:
    preset: int

    def __post_init__(self) -> None:
        if self.preset < 0:
            raise ValueError(
                "Preset cannot be negative."
            )