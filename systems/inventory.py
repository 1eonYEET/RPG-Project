from typing import Dict, List, Type
from items.equipment import Equipment, StatModifier

class Inventory:
    """
    Passive, stapelnde Item-Effekte.
    Heiltränke werden NICHT hier verwaltet, aber in list_items() mit angezeigt (über owner.heal_potions),
    damit die Inventaransicht vollständig ist.
    """
    def __init__(self, owner):
        self.owner = owner
        self._items: Dict[Type[Equipment], tuple[Equipment, int]] = {}

    # ---------- Verwaltung ----------
    def add_item(self, item: Equipment, qty: int = 1):
        if qty <= 0:
            return
        proto, count = self._items.get(type(item), (item, 0))
        self._items[type(item)] = (proto, count + qty)
        for _ in range(qty):
            self._apply(proto.mod, invert=False)

    def remove_item(self, item_type: Type[Equipment], qty: int = 1) -> bool:
        if item_type not in self._items or qty <= 0:
            return False
        proto, count = self._items[item_type]
        if count < qty:
            return False
        for _ in range(qty):
            self._apply(proto.mod, invert=True)
        new_qty = count - qty
        if new_qty == 0:
            del self._items[item_type]
        else:
            self._items[item_type] = (proto, new_qty)
        return True

    # ---------- Anzeige ----------
    def list_items(self) -> List[str]:
        """
        Listet NUR passive Ausrüstungs-Items (mit Stacks) – KEINE Heiltränke.
        Heiltränke werden bewusst außerhalb (z. B. in player._show_inventory / shop._show_inventory)
        angezeigt, damit sie nicht doppelt auftauchen.
        """
        lines: List[str] = []
        for proto, qty in self._items.values():
            lines.append(f"{proto.name()} x{qty} — {proto.description()}")
        return lines

    def is_empty(self) -> bool:
        return len(self._items) == 0

    # ---------- Interne Stat-Anpassung (+ Caps) ----------
    def _apply(self, m: StatModifier, invert: bool):
        s = -1 if invert else 1

        # Additiv
        self.owner.max_hp += s * m.hp
        if s > 0:
            self.owner.hp += s * m.hp
        self.owner.hp = min(self.owner.hp, self.owner.max_hp)

        self.owner.attack  += s * m.attack
        self.owner.defense += s * m.defense

        self.owner.max_mana += s * m.mana
        if s > 0:
            self.owner.mana += s * m.mana
        self.owner.mana = min(self.owner.mana, self.owner.max_mana)

        # Caps
        self.owner.armor        = max(0.0, min(0.8, self.owner.armor + s * m.armor_add))
        self.owner.crit_chance  = max(0.0, min(1.0, self.owner.crit_chance + s * m.crit_add))
        self.owner.dodge_chance = max(0.0, min(0.6, self.owner.dodge_chance + s * m.dodge_add))

        if hasattr(self.owner, "spell_power"):
            self.owner.spell_power += s * m.spell_power_mul
        if hasattr(self.owner, "heal_power"):
            self.owner.heal_power += s * m.heal_power_mul
