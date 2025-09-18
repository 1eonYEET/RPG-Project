from items.equipment import Equipment, StatModifier
from items.equipment_slots import Slot

class LeatherArmor(Equipment):
    def __init__(self):
        super().__init__(
            Slot.ARMOR,
            StatModifier(defense=1, armor_add=0.05, dodge_add=0.02)
        )

    def name(self) -> str:
        return "Lederharnisch"

    def description(self) -> str:
        return "+1 DEF, +5% Rüstung, +2% Ausweichen."
