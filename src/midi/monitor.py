```python
from collections.abc import Callable

from mido import Message

from .interface import MidiInput

class MidiMonitor:
    def __init__(
        self,
        midi_input: MidiInput,
        message_handler: Callable[[Message], None] | None = None,
    ) -> None:
        self._midi_input = midi_input
        self._message_handler = message_handler or self._default_handler

    def start(self) -> None:
        if self._midi_input.is_open():
            return

        self._midi_input.open()

        try:
            while self._midi_input.is_open():
                for message in self._midi_input.messages():
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
        print(
            f"MIDI RX | "
            f"type={message.type} | "
            f"message={message}"
        )
```
