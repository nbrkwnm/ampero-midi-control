import pytest

from ampero.commands import ToggleEffect
from ampero.protocol.ampero_ii_stomp_reference import (
    create_reference_specification,
)
from ampero.protocol.midi_protocol import MidiAmperoProtocol

def create_protocol() -> MidiAmperoProtocol:
    return MidiAmperoProtocol(
        specification=create_reference_specification(),
    )

def test_toggle_effect_on() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        ToggleEffect(
            effect="effect_1",
            enabled=True,
        )
    )

    assert len(messages) == 1
    assert messages[0].type == "control_change"
    assert messages[0].channel == 0
    assert messages[0].control == 48
    assert messages[0].value == 127

def test_toggle_effect_off() -> None:
    protocol = create_protocol()

    messages = protocol.encode(
        ToggleEffect(
            effect="effect_1",
            enabled=False,
        )
    )

    assert len(messages) == 1
    assert messages[0].type == "control_change"
    assert messages[0].channel == 0
    assert messages[0].control == 48
    assert messages[0].value == 0

def test_toggle_effect_rejects_unknown_effect() -> None:
    protocol = create_protocol()

    with pytest.raises(ValueError):
        protocol.encode(
            ToggleEffect(
                effect="unknown",
                enabled=True,
            )
        )