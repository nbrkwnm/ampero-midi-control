from dataclasses import dataclass

@dataclass(frozen=True)
class BankUp:
    pass

@dataclass(frozen=True)
class BankDown:
    pass

@dataclass(frozen=True)
class PatchUp:
    pass

@dataclass(frozen=True)
class PatchDown:
    pass