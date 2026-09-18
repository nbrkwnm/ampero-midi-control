from ampero.commands.navigation import (
    BankDown,
    BankUp,
    PatchDown,
    PatchUp,
)

def test_bank_up_can_be_created() -> None:
    assert BankUp() is not None

def test_bank_down_can_be_created() -> None:
    assert BankDown() is not None

def test_patch_up_can_be_created() -> None:
    assert PatchUp() is not None

def test_patch_down_can_be_created() -> None:
    assert PatchDown() is not None