from items.equipment import Equipment, StatModifier
from items.equipment_slots import Slot

class ManaCrystal(Equipment):
    def __init__(self):
        super().__init__(
            Slot.ACCESSORY,
            StatModifier(mana=3, spell_power_mul=0.1)
        )

    def name(self) -> str:
        return "Mana-Kristall"

    def description(self) -> str:
        return "+5 Max Mana, +10% Zauberkraft."
