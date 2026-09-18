import pytest

from ampero.commands import SelectPreset

def test_select_preset_accepts_valid_preset() -> None:
    command = SelectPreset(
        preset=10,
    )

    assert command.preset == 10

def test_select_preset_rejects_negative_preset() -> None:
    with pytest.raises(ValueError):
        SelectPreset(
            preset=-1,
        )