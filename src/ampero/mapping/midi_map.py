from dataclasses import dataclass

@dataclass(frozen=True)
class MidiMapping:
    channel: int
    control: int
    value_on: int
    value_off: int