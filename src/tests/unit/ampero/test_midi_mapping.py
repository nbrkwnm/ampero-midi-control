from ampero.mapping.midi_map import MidiMapping
from midi.message_type import MidiMessageType

def test_control_change_mapping() -> None:
    mapping = MidiMapping(
        message_type=MidiMessageType.CONTROL_CHANGE,
        channel=0,
        control=20,
        value_on=127,
        value_off=0,
    )

    assert mapping.message_type == MidiMessageType.CONTROL_CHANGE
    assert mapping.channel == 0
    assert mapping.control == 20
    assert mapping.value_on == 127
    assert mapping.value_off == 0

def test_program_change_mapping() -> None: 
    mapping = MidiMapping( 
        message_type=MidiMessageType.PROGRAM_CHANGE, 
        channel=0, 
        program=5, ) 
        
    assert mapping.message_type == MidiMessageType.PROGRAM_CHANGE 
    assert mapping.channel == 0 
    assert mapping.program == 5