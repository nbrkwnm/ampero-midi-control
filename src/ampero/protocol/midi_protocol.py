from dataclasses import replace

from mido import Message

from ampero.commands import SelectPreset, ToggleEffect
from ampero.protocol.base import AmperoProtocol
from ampero.protocol.preset_resolver import PresetResolver
from ampero.protocol.specification import (
    AmperoMiniMidiSpecification,
    MidiCommandMapping,
)
from midi.message_factory import MidiMessageFactory
from midi.message_type import MidiMessageType

class MidiAmperoProtocol(AmperoProtocol):
    def __init__(
        self,
        specification: AmperoMiniMidiSpecification,
    ) -> None:
        self._specification = specification
        self._preset_resolver = PresetResolver(
            presets_per_bank=specification.presets_per_bank,
        )

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
        sequence = self._specification.preset_mapping

        if sequence is None:
            raise RuntimeError(
                "Preset MIDI mapping is not configured."
            )

        resolved_preset = self._preset_resolver.resolve(
            command.preset,
        )

        messages: list[Message] = []

        for mapping in sequence.messages:
            resolved_mapping = self._resolve_preset_mapping(
                mapping,
                resolved_preset.bank,
                resolved_preset.program,
            )

            messages.append(
                MidiMessageFactory.from_mapping(
                    resolved_mapping
                )
            )

        return messages

    def _resolve_preset_mapping(
        self,
        mapping: MidiCommandMapping,
        bank: int,
        program: int,
    ) -> MidiCommandMapping:
        if mapping.message_type == MidiMessageType.PROGRAM_CHANGE:
            return replace(
                mapping,
                program=program,
            )

        if (
            mapping.message_type
            == MidiMessageType.CONTROL_CHANGE
            and mapping.control == 0
        ):
            return replace(
                mapping,
                value=bank,
            )

        return mapping

    def _encode_toggle_effect(
        self,
        command: ToggleEffect,
    ) -> list[Message]:
        mapping = self._specification.effect_mappings

        if mapping is None:
            raise RuntimeError(
                "Effect MIDI mappings are not configured."
            )

        effect_mapping = mapping.get(command.effect)

        if effect_mapping is None:
            raise ValueError(
                f"Unknown effect: {command.effect}"
            )

        if effect_mapping.message_type != MidiMessageType.CONTROL_CHANGE:
            raise ValueError(
                "Effect mapping must use Control Change."
            )

        if effect_mapping.value is not None:
            raise ValueError(
                "Effect mapping must not define a fixed value."
            )

        resolved_mapping = replace(
            effect_mapping,
            value=127 if command.enabled else 0,
        )

        return [
            MidiMessageFactory.from_mapping(
                resolved_mapping
            )
        ]