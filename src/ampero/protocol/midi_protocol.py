from mido import Message

from ampero.commands import SelectPreset, ToggleEffect
from ampero.mapping.midi_map import MidiMapping
from ampero.protocol.base import AmperoProtocol

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

        return [
            Message(
                "control_change",
                channel=self._preset_mapping.channel,
                control=self._preset_mapping.control,
                value=command.preset,
            )
        ]

    def _encode_toggle_effect(
        self,
        command: ToggleEffect,
    ) -> list[Message]:
        raise NotImplementedError(
            "Effect MIDI mapping is not implemented."
        )