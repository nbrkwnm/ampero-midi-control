import pytest

from ampero.commands import SelectPreset
from ampero.protocol.ampero_ii_stomp_reference import (
    create_reference_specification,
)
from ampero.protocol.midi_protocol import MidiAmperoProtocol
from ampero.protocol.preset_resolver import PresetResolver
from ampero.protocol.specification import AmperoMiniMidiSpecification

def create_protocol() -> MidiAmperoProtocol:
    return MidiAmperoProtocol(
        specification=create_reference_specification(),
    )

def test_select_preset_requires_mapping() -> None:
    protocol = MidiAmperoProtocol(
        specification=AmperoMiniMidiSpecification(
            presets_per_bank=10,
        ),
    )

    with pytest.raises(RuntimeError):
        protocol.encode(
            SelectPreset(preset=0),
        )

def test_select_preset_generates_reference_sequence() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        SelectPreset(preset=5),
    )

    assert len(messages) == 2

    assert messages[0].type == "control_change"
    assert messages[0].channel == 0
    assert messages[0].control == 0
    assert messages[0].value == 0

    assert messages[1].type == "program_change"
    assert messages[1].channel == 0
    assert messages[1].program == 5

def test_select_preset_resolves_bank_and_program() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        SelectPreset(preset=12),
    )

    assert len(messages) == 2

    assert messages[0].type == "control_change"
    assert messages[0].control == 0
    assert messages[0].value == 1

    assert messages[1].type == "program_change"
    assert messages[1].program == 2

def test_select_preset_uses_requested_program() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        SelectPreset(preset=42),
    )

    assert messages[1].type == "program_change"
    assert messages[1].program == 2

def test_select_preset_preserves_message_order() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        SelectPreset(preset=5),
    )

    assert [message.type for message in messages] == [
        "control_change",
        "program_change",
    ]

def test_unsupported_command_is_rejected() -> None:
    protocol = create_protocol()

    with pytest.raises(TypeError):
        protocol.encode(
            object(),
        )

def test_select_preset_rejects_negative_preset() -> None:
    protocol = create_protocol()

    with pytest.raises(ValueError):
        protocol.encode(
            SelectPreset(preset=-1),
        )