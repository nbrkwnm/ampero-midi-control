from collections.abc import Callable
from datetime import datetime

from mido import Message

from .interface import MidiInput
from .message_formatter import MidiMessageFormatter

class MidiMonitor:
    def __init__(
        self,
        midi_input: MidiInput,
        message_handler: Callable[[Message], None] | None = None,
    ) -> None:
        self._midi_input = midi_input
        self._message_handler = (
            message_handler or self._default_handler
        )

    def start(self) -> None:
        if self._midi_input.is_open():
            return

        self._midi_input.open()

        try:
            for message in self._midi_input.messages():
                if not self._midi_input.is_open():
                    break

                self._message_handler(message)

        except KeyboardInterrupt:
            pass

        finally:
            self.stop()

    def stop(self) -> None:
        if self._midi_input.is_open():
            self._midi_input.close()

    @staticmethod
    def _default_handler(message: Message) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted = MidiMessageFormatter.format(message)
        raw = MidiMessageFormatter.raw(message)

        print(
            f"{timestamp} | RX | {formatted} | RAW={raw}"
        )