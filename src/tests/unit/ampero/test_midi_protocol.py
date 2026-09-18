import pytest

from ampero.commands import SelectPreset
from ampero.mapping.midi_map import MidiMapping
from ampero.protocol.midi_protocol import MidiAmperoProtocol
from midi.message_type import MidiMessageType

def test_select_preset_requires_mapping() -> None:
    protocol = MidiAmperoProtocol()

    command = SelectPreset(
        preset=5,
    )

    with pytest.raises(RuntimeError):
        protocol.encode(command)

def test_select_preset_generates_control_change() -> None:
    mapping = MidiMapping(
        message_type=MidiMessageType.CONTROL_CHANGE,
        channel=0,
        control=20,
    )

    protocol = MidiAmperoProtocol(
        preset_mapping=mapping,
    )

    command = SelectPreset(
        preset=5,
    )

    messages = protocol.encode(
        command,
    )

    assert len(messages) == 1

    message = messages[0]

    assert message.type == "control_change"
    assert message.channel == 0
    assert message.control == 20
    assert message.value == 5

def test_unsupported_command_is_rejected() -> None:
    protocol = MidiAmperoProtocol()

    with pytest.raises(TypeError):
        protocol.encode(
            object(),
        )

def test_select_preset_generates_program_change() -> None:
    mapping = MidiMapping(
        message_type=MidiMessageType.PROGRAM_CHANGE,
        channel=0,
        program=5,
    )

    protocol = MidiAmperoProtocol(
        preset_mapping=mapping,
    )

    command = SelectPreset(
        preset=5,
    )

    messages = protocol.encode(
        command,
    )

    assert len(messages) == 1

    message = messages[0]

    assert message.type == "program_change"
    assert message.channel == 0
    assert message.program == 5