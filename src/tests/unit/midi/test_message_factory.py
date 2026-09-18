from mido import Message

from midi.message_factory import MidiMessageFactory

def test_control_change() -> None:
    message = MidiMessageFactory.control_change(
        channel=0,
        control=20,
        value=127,
    )

    assert message == Message(
        "control_change",
        channel=0,
        control=20,
        value=127,
    )

def test_program_change() -> None:
    message = MidiMessageFactory.program_change(
        channel=0,
        program=5,
    )

    assert message == Message(
        "program_change",
        channel=0,
        program=5,
    )

def test_note_on() -> None:
    message = MidiMessageFactory.note_on(
        channel=0,
        note=60,
        velocity=127,
    )

    assert message == Message(
        "note_on",
        channel=0,
        note=60,
        velocity=127,
    )

def test_note_off() -> None:
    message = MidiMessageFactory.note_off(
        channel=0,
        note=60,
        velocity=0,
    )

    assert message == Message(
        "note_off",
        channel=0,
        note=60,
        velocity=0,
    )