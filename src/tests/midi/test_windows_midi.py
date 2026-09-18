from mido import Message

from infrastructure.midi.windows_midi import (
    WindowsMidiDeviceProvider,
)

def test_midi_output_can_be_created() -> None:
    provider = WindowsMidiDeviceProvider()

    ports = provider.output_ports()

    assert ports

def test_midi_message_can_be_created() -> None:
    message = Message(
        "control_change",
        channel=0,
        control=20,
        value=127,
    )

    assert message.type == "control_change"
    assert message.channel == 0
    assert message.control == 20
    assert message.value == 127
