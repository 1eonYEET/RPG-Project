from abc import ABC, abstractmethod
from dataclasses import dataclass
from items.equipment_slots import Slot

@dataclass
class StatModifier:
    # Additive Stats
    hp: int = 0
    attack: int = 0
    defense: int = 0
    mana: int = 0
    # Additive Wahrscheinlichkeiten/Prozente
    armor_add: float = 0.0       # +0.05 -> +5% Schadensreduktion
    crit_add: float = 0.0        # +0.05 -> +5% Kritchance
    dodge_add: float = 0.0       # +0.03 -> +3% Ausweichchance
    # Multiplikatoren (optional)
    spell_power_mul: float = 0.0
    heal_power_mul: float = 0.0

class Equipment(ABC):
    def __init__(self, slot: Slot, mod: StatModifier):
        self.slot = slot
        self.mod = mod

    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def description(self) -> str: ...
