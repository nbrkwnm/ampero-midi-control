from mido import Message

class FakeMidiOutput:
    def __init__(self) -> None:
        self.opened = False
        self.sent_messages: list[Message] = []

    def open(self) -> None:
        self.opened = True

    def close(self) -> None:
        self.opened = False

    def send(self, message: Message) -> None:
        if not self.opened:
            raise RuntimeError(
                "MIDI output is not open."
            )

        self.sent_messages.append(message)

    def is_open(self) -> bool:
        return self.opened