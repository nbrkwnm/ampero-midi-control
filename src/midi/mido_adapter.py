from collections.abc import Callable, Iterator

import mido
from mido import Message

from .interface import MidiDeviceProvider, MidiInput, MidiOutput

class MidoInput(MidiInput):
    def __init__(
        self,
        port_name: str,
        callback: Callable[[Message], None] | None = None,
    ) -> None:
        self._port_name = port_name
        self._callback = callback
        self._port = None

    def open(self) -> None:
        if self._port is not None:
            return

        self._port = mido.open_ioport(
            self._port_name,
            callback=self._callback,
        )

    def close(self) -> None:
        if self._port is None:
            return

        self._port.close()
        self._port = None

    def messages(self) -> Iterator[Message]:
        if self._port is None:
            raise RuntimeError("MIDI input is not open.")

        yield from self._port.iter_pending()

    def is_open(self) -> bool:
        return self._port is not None


class MidoOutput(MidiOutput):
    def __init__(self, port_name: str) -> None:
        self._port_name = port_name
        self._port = None

    def open(self) -> None:
        if self._port is not None:
            return

        self._port = mido.open_output(self._port_name)

    def close(self) -> None:
        if self._port is None:
            return

        self._port.close()
        self._port = None

    def send(self, message: Message) -> None:
        if self._port is None:
            raise RuntimeError("MIDI output is not open.")

        self._port.send(message)

    def is_open(self) -> bool:
        return self._port is not None


class MidoDeviceProvider(MidiDeviceProvider):
    def input_ports(self) -> list[str]:
        return list(mido.get_input_names())

    def output_ports(self) -> list[str]:
        return list(mido.get_output_names())

    def create_input(
        self,
        port_name: str,
        callback: Callable[[Message], None] | None = None,
    ) -> MidiInput:
        return MidoInput(port_name, callback)

    def create_output(self, port_name: str) -> MidiOutput:
        return MidoOutput(port_name)
```
