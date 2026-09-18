from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator

from mido import Message

class MidiInput(ABC):
    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def messages(self) -> Iterator[Message]:
        raise NotImplementedError

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

class MidiOutput(ABC):
    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def send(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

class MidiDeviceProvider(ABC):
    @abstractmethod
    def input_ports(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def output_ports(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def create_input(
        self,
        port_name: str,
        callback: Callable[[Message], None] | None = None,
    ) -> MidiInput:
        raise NotImplementedError

    @abstractmethod
    def create_output(self, port_name: str) -> MidiOutput:
        raise NotImplementedError