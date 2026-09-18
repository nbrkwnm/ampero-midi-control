from mido import Message

class MidiMessageFactory:
    @staticmethod
    def control_change(
        channel: int,
        control: int,
        value: int,
    ) -> Message:
        return Message(
            "control_change",
            channel=channel,
            control=control,
            value=value,
        )

    @staticmethod
    def program_change(
        channel: int,
        program: int,
    ) -> Message:
        return Message(
            "program_change",
            channel=channel,
            program=program,
        )

    @staticmethod
    def note_on(
        channel: int,
        note: int,
        velocity: int,
    ) -> Message:
        return Message(
            "note_on",
            channel=channel,
            note=note,
            velocity=velocity,
        )

    @staticmethod
    def note_off(
        channel: int,
        note: int,
        velocity: int,
    ) -> Message:
        return Message(
            "note_off",
            channel=channel,
            note=note,
            velocity=velocity,
        )