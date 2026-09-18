from mido import Message

from ampero.protocol.specification import MidiCommandMapping
from midi.message_type import MidiMessageType

class MidiMessageFactory:
    @staticmethod
    def from_mapping(
        mapping: MidiCommandMapping,
    ) -> Message:
        if mapping.message_type == MidiMessageType.CONTROL_CHANGE:
            if mapping.control is None:
                raise ValueError(
                    "Control Change mapping requires a control number."
                )

            if mapping.value is None:
                raise ValueError(
                    "Control Change mapping requires a value."
                )

            return MidiMessageFactory.control_change(
                channel=mapping.channel,
                control=mapping.control,
                value=mapping.value,
            )

        if mapping.message_type == MidiMessageType.PROGRAM_CHANGE:
            if mapping.program is None:
                raise ValueError(
                    "Program Change mapping requires a program number."
                )

            return MidiMessageFactory.program_change(
                channel=mapping.channel,
                program=mapping.program,
            )

        if mapping.message_type == MidiMessageType.NOTE_ON:
            if mapping.control is None:
                raise ValueError(
                    "Note On mapping requires a note number."
                )

            if mapping.value is None:
                raise ValueError(
                    "Note On mapping requires a velocity."
                )

            return MidiMessageFactory.note_on(
                channel=mapping.channel,
                note=mapping.control,
                velocity=mapping.value,
            )

        if mapping.message_type == MidiMessageType.NOTE_OFF:
            if mapping.control is None:
                raise ValueError(
                    "Note Off mapping requires a note number."
                )

            if mapping.value is None:
                raise ValueError(
                    "Note Off mapping requires a velocity."
                )

            return MidiMessageFactory.note_off(
                channel=mapping.channel,
                note=mapping.control,
                velocity=mapping.value,
            )

        raise ValueError(
            f"Unsupported MIDI message type: {mapping.message_type}"
        )

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