from dataclasses import dataclass

@dataclass(frozen=True)
class ResolvedPreset:
    bank: int
    program: int

class PresetResolver:
    def __init__(
        self,
        presets_per_bank: int,
    ) -> None:
        if presets_per_bank <= 0:
            raise ValueError(
                "presets_per_bank must be greater than zero."
            )

        self._presets_per_bank = presets_per_bank

    def resolve(
        self,
        preset: int,
    ) -> ResolvedPreset:
        if preset < 0:
            raise ValueError(
                "Preset must be greater than or equal to zero."
            )

        bank = preset // self._presets_per_bank
        program = preset % self._presets_per_bank

        return ResolvedPreset(
            bank=bank,
            program=program,
        )