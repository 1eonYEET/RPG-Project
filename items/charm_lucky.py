from items.equipment import Equipment, StatModifier
from items.equipment_slots import Slot

class LuckyCharm(Equipment):
    def __init__(self):
        super().__init__(
            Slot.ACCESSORY,
            StatModifier(crit_add=0.05, dodge_add=0.03)
        )

    def name(self) -> str:
        return "Glücksanhänger"

    def description(self) -> str:
        return "+5% Krit, +3% Ausweichen."
