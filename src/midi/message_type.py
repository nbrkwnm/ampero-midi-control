from enum import Enum

class MidiMessageType(Enum):
    CONTROL_CHANGE = "control_change"
    PROGRAM_CHANGE = "program_change"
    NOTE_ON = "note_on"
    NOTE_OFF = "note_off"
    SYSEX = "sysex"