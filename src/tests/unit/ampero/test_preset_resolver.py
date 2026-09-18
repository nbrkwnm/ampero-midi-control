import pytest

from ampero.protocol.preset_resolver import PresetResolver

def test_resolve_first_preset() -> None:
    resolver = PresetResolver(
        presets_per_bank=10,
    )

    result = resolver.resolve(0)

    assert result.bank == 0
    assert result.program == 0

def test_resolve_last_preset_of_first_bank() -> None:
    resolver = PresetResolver(
        presets_per_bank=10,
    )

    result = resolver.resolve(9)

    assert result.bank == 0
    assert result.program == 9

def test_resolve_first_preset_of_second_bank() -> None:
    resolver = PresetResolver(
        presets_per_bank=10,
    )

    result = resolver.resolve(10)

    assert result.bank == 1
    assert result.program == 0

def test_resolve_rejects_negative_preset() -> None:
    resolver = PresetResolver(
        presets_per_bank=10,
    )

    with pytest.raises(ValueError):
        resolver.resolve(-1)

def test_resolver_rejects_invalid_bank_size() -> None:
    with pytest.raises(ValueError):
        PresetResolver(
            presets_per_bank=0,
        )