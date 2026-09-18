from mido import Message

from ampero.protocol.base import AmperoProtocol
from midi.interface import MidiOutput

class AmperoController:
    def __init__(
        self,
        midi_output: MidiOutput,
        protocol: AmperoProtocol,
    ) -> None:
        self._midi_output = midi_output
        self._protocol = protocol

    def connect(self) -> None:
        self._midi_output.open()

    def disconnect(self) -> None:
        self._midi_output.close()

    def execute(self, command: object) -> None:
        messages = self._protocol.encode(command)

        for message in messages:
            self._send(message)

    def send_message(self, message: Message) -> None:
        self._send(message)

    def _send(self, message: Message) -> None:
        self._midi_output.send(message)