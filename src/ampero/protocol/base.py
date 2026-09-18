from abc import ABC, abstractmethod

from mido import Message


class AmperoProtocol(ABC):
    @abstractmethod
    def decode(self, message: Message) -> object | None:
        raise NotImplementedError

    @abstractmethod
    def encode(self, command: object) -> list[Message]:
        raise NotImplementedError