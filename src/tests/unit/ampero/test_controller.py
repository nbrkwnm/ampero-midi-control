from mido import Message

from ampero.controller import AmperoController
from tests.fakes.fake_midi_output import FakeMidiOutput

class FakeProtocol:
    def __init__(self) -> None:
        self.commands = []

    def encode(self, command: object) -> list[Message]:
        self.commands.append(command)

        return [
            Message(
                "control_change",
                channel=0,
                control=10,
                value=127,
            )
        ]

    def decode(self, message: Message) -> object | None:
        return None

def test_controller_opens_output() -> None:
    output = FakeMidiOutput()
    protocol = FakeProtocol()

    controller = AmperoController(
        output,
        protocol,
    )

    controller.connect()

    assert output.is_open()

def test_controller_closes_output() -> None:
    output = FakeMidiOutput()
    protocol = FakeProtocol()

    controller = AmperoController(
        output,
        protocol,
    )

    controller.connect()
    controller.disconnect()

    assert not output.is_open()

def test_controller_encodes_and_sends_command() -> None:
    output = FakeMidiOutput()
    protocol = FakeProtocol()

    controller = AmperoController(
        output,
        protocol,
    )

    controller.connect()

    command = object()

    controller.execute(command)

    assert protocol.commands == [command]

    assert output.sent_messages == [
        Message(
            "control_change",
            channel=0,
            control=10,
            value=127,
        )
    ]