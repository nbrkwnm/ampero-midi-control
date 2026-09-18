from dataclasses import dataclass

from midi.message_type import MidiMessageType

@dataclass(frozen=True)
class MidiCommandMapping:
    message_type: MidiMessageType
    channel: int
    control: int | None = None
    value: int | None = None
    program: int | None = None

@dataclass(frozen=True)
class MidiCommandSequence:
    messages: tuple[MidiCommandMapping, ...]

@dataclass(frozen=True)
class AmperoMiniMidiSpecification:
    presets_per_bank: int
    preset_mapping: MidiCommandSequence | None = None
    bank_down_mapping: MidiCommandMapping | None = None
    bank_up_mapping: MidiCommandMapping | None = None
    patch_down_mapping: MidiCommandMapping | None = None
    patch_up_mapping: MidiCommandMapping | None = None
    expression_mapping: MidiCommandMapping | None = None
    expression_switch_mapping: MidiCommandMapping | None = None
    effect_mappings: dict[str, MidiCommandMapping] | None = None

    def __post_init__(self) -> None:
        if self.presets_per_bank <= 0:
            raise ValueError(
                "presets_per_bank must be greater than zero."
            )