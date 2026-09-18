from mido import Message

from ampero.commands import SelectPreset, ToggleEffect
from ampero.mapping.midi_map import MidiMapping
from ampero.protocol.base import AmperoProtocol
from midi.message_factory import MidiMessageFactory
from midi.message_type import MidiMessageType

class MidiAmperoProtocol(AmperoProtocol):
    def __init__(
        self,
        preset_mapping: MidiMapping | None = None,
    ) -> None:
        self._preset_mapping = preset_mapping

    def decode(self, message: Message) -> object | None:
        return None

    def encode(self, command: object) -> list[Message]:
        if isinstance(command, SelectPreset):
            return self._encode_select_preset(command)

        if isinstance(command, ToggleEffect):
            return self._encode_toggle_effect(command)

        raise TypeError(
            f"Unsupported command: {type(command).__name__}"
        )

    def _encode_select_preset(
        self,
        command: SelectPreset,
    ) -> list[Message]:
        if self._preset_mapping is None:
            raise RuntimeError(
                "Preset MIDI mapping is not configured."
            )

        mapping = self._preset_mapping

        if mapping.message_type == MidiMessageType.CONTROL_CHANGE:
            return [
                MidiMessageFactory.control_change(
                    channel=mapping.channel or 0,
                    control=mapping.control or 0,
                    value=command.preset,
                )
            ]

        if mapping.message_type == MidiMessageType.PROGRAM_CHANGE:
            return [
                MidiMessageFactory.program_change(
                    channel=mapping.channel or 0,
                    program=command.preset,
                )
            ]

        raise ValueError(
            "Unsupported MIDI message type for preset."
        )

    def _encode_toggle_effect(
        self,
        command: ToggleEffect,
    ) -> list[Message]:
        raise NotImplementedError(
            "Effect MIDI mapping is not implemented."
        )