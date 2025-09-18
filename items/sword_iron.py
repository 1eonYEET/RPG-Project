from items.equipment import Equipment, StatModifier
from items.equipment_slots import Slot

class IronSword(Equipment):
    def __init__(self):
        super().__init__(
            Slot.WEAPON,
            StatModifier(attack=3, crit_add=0.02)
        )

    def name(self) -> str:
        return "Eisenschwert"

    def description(self) -> str:
        return "+3 ATK, +2% Krit."
