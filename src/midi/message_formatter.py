from mido import Message

class MidiMessageFormatter:
    @staticmethod
    def format(message: Message) -> str:
        data = MidiMessageFormatter._data(message)

        return (
            f"type={message.type} "
            f"{data}"
        )

    @staticmethod
    def raw(message: Message) -> str:
        return " ".join(
            f"{byte:02X}"
            for byte in message.bytes()
        )

    @staticmethod
    def _data(message: Message) -> str:
        attributes = []

        for attribute in (
            "channel",
            "note",
            "velocity",
            "control",
            "value",
            "program",
            "pitch",
            "pos",
            "song",
            "frame_type",
            "frame",
            "sysex",
        ):
            if hasattr(message, attribute):
                attributes.append(
                    f"{attribute}={getattr(message, attribute)}"
                )

        return " ".join(attributes)
