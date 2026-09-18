from dataclasses import dataclass

from midi.message_type import MidiMessageType

@dataclass(frozen=True)
class MidiMapping:
    message_type: MidiMessageType
    channel: int | None = None
    control: int | None = None
    value_on: int | None = None
    value_off: int | None = None
    program: int | None = None