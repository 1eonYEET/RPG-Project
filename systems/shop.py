# systems/shop.py
from dataclasses import dataclass
from typing import Callable, List, Union

from items.mana_crystal import ManaCrystal
from systems.inventory import Inventory
from items.sword_iron import IronSword
from items.armor_leather import LeatherArmor
from items.charm_lucky import LuckyCharm
from items.equipment import StatModifier
from skilltree.effects import EffectApplier
from skilltree.schema import AddStatsEffect


# ---------------------- Angebots-Typen ----------------------

@dataclass
class ItemOffer:
    name: str
    description: str
    price: int
    ctor: Callable  # Konstruktor der Itemklasse, z. B. IronSword

@dataclass
class PotionOffer:
    name: str
    description: str
    price: int  # Preis pro Trank

Offer = Union[ItemOffer, PotionOffer]


# --------------------------- Shop ---------------------------

class Shop:
    """
    Shop mit:
    - passiven, stackenden Ausrüstungs-Items (via Inventory.add_item)
    - Heiltränken (Consumable, zählen in player.heal_potions)
    - Mengen-Kauf (Eingabe z. B. '2x3')
    - tier-basiertem Preisfaktor (früh günstiger, später teurer)
    - Vorher→Nachher-Preview je Angebot (pro Stück) + nach Kauf für die Menge
    """

    def __init__(self):
        self.offers: List[Offer] = [
            ItemOffer("Eisenschwert",   "+3 ATK, +2% Krit.",              60, IronSword),
            ItemOffer("Lederharnisch",  "+1 DEF, +5% Rüstung, +2% Dodge", 75, LeatherArmor),
            ItemOffer("Glücksanhänger", "+5% Krit, +3% Dodge",            90, LuckyCharm),
            PotionOffer("Heiltrank",    "Heilt 20 HP (skaliert mit Heilbonus)", 35),
            ItemOffer("Mana-Kristall",   "+5 Max Mana, +10% Zauberkraft.", 80, ManaCrystal)
        ]
        self._applier = EffectApplier()

    # ---------------------- Public API ----------------------

    def open(self, player, notifier, tier: int = 0):
        """
        Öffnet den Shop. 'tier' beeinflusst die Preise (früh → günstiger, später → teurer).
        Zeigt Vorher→Nachher je Angebot (pro 1 Stück).
        """
        inv: Inventory = player.inventory
        mul = self._price_multiplier(tier)

        notifier.notify("\n🏪 Shop geöffnet! (Items passiv & stackend, Heiltränke verbrauchbar)")
        notifier.notify(f"💰 Dein Gold: {player.gold}g  |  Preisfaktor: x{mul:.2f}")

        while True:
            print("\nAngebote:")
            for i, o in enumerate(self.offers, start=1):
                price = self._price_for_offer(o, mul)
                preview = self._offer_preview(player, o)  # pro Einheit
                suffix = f"  ({preview})" if preview else ""
                print(f"{i}. {o.name} — {o.description} — {price}g{suffix}")
            print("I. Inventar ansehen")
            print("0. Schließen")

            choice = input("Kaufe (Nummer) / I für Inventar: ").strip().lower()

            if choice in ("0", ""):
                notifier.notify("🧾 Shop geschlossen.")
                return

            if choice == "i":
                self._show_inventory(player)
                continue

            offer_idx, qty = self._parse_selection(choice)
            if offer_idx is None or qty is None:
                notifier.notify("❌ Ungültige Eingabe.")
                continue

            try:
                offer = self.offers[offer_idx]
            except IndexError:
                notifier.notify("❌ Ungültige Angebotsnummer.")
                continue

            unit_price = self._price_for_offer(offer, mul)
            total_cost = unit_price * qty

            if player.gold < total_cost:
                notifier.notify(f"💸 Nicht genug Gold ({player.gold}g). Benötigt: {total_cost}g.")
                continue

            # Kauf durchführen
            # Vorher Snapshot für Mengen-Preview
            before_snapshot = self._snapshot(player)
            player.gold -= total_cost

            if isinstance(offer, ItemOffer):
                inv.add_item(offer.ctor(), qty=qty)
                after_preview = self._delta_preview_from_snapshot(player, before_snapshot)
                suffix = f" | " + " | ".join(after_preview) if after_preview else ""
                notifier.notify(f"✅ Gekauft: {offer.name} x{qty} für {total_cost}g. Verbleibend: {player.gold}g{suffix}")
            else:  # PotionOffer
                old = getattr(player, "heal_potions", 0)
                player.heal_potions = old + qty
                notifier.notify(
                    f"✅ Gekauft: Heiltrank x{qty} für {total_cost}g. "
                    f"(Tränke: x{old} -> x{player.heal_potions}) | Verbleibend: {player.gold}g"
                )

    # ---------------------- Internals -----------------------

    def _price_multiplier(self, tier: int) -> float:
        if tier <= 0: return 0.90
        if tier == 1: return 1.00
        if tier == 2: return 1.10
        if tier == 3: return 1.20
        return min(1.25 + 0.03 * (tier - 4), 1.50)

    def _price_for_offer(self, offer: Offer, mul: float) -> int:
        return int(round(offer.price * mul))

    def _show_inventory(self, player):
        inv = player.inventory
        print("\n🎒 INVENTAR:")
        if getattr(player, "heal_potions", 0) > 0:
            print(f"  Heiltrank x{player.heal_potions} — Heilt 20 HP (skaliert mit Heilbonus)")
        if inv.is_empty() and getattr(player, "heal_potions", 0) <= 0:
            print("  – leer –")
            return
        for line in inv.list_items():
            print(" ", line)

    def _parse_selection(self, raw: str):
        parts = raw.split("x")
        try:
            idx = int(parts[0]) - 1
        except ValueError:
            return None, None
        qty = 1
        if len(parts) == 2:
            try:
                qty = max(1, int(parts[1]))
            except ValueError:
                return None, None
        return idx, qty

    # ---------- Preview-Helfer ----------

    def _offer_preview(self, player, offer: Offer) -> str:
        """
        Liefert eine kurze 1-Stück-Preview: 'ATK: 10 -> 13 | Krit: 12% -> 14%'.
        Für Potions: 'Tränke: x3 -> x4'.
        """
        if isinstance(offer, PotionOffer):
            cur = getattr(player, "heal_potions", 0)
            return f"Tränke: x{cur} -> x{cur+1}"
        # Item → StatModifier zu AddStatsEffect mappen
        proto = offer.ctor()
        eff = self._map_statmod_to_effect(proto.mod)
        lines = self._applier.preview(player, eff)
        return " | ".join(lines)

    def _map_statmod_to_effect(self, m: StatModifier) -> AddStatsEffect:
        return AddStatsEffect(
            hp=m.hp,
            attack=m.attack,
            defense=m.defense,
            mana=m.mana,
            armor_add=m.armor_add,
            crit_add=m.crit_add,
            dodge_add=m.dodge_add,
            spell_power=m.spell_power_mul,
            heal_power=m.heal_power_mul,
        )

    def _snapshot(self, player):
        """Kleiner Snapshot der wichtigen Stats vor dem Kauf (für Mengen-Preview)."""
        return dict(
            max_hp=getattr(player, "max_hp", 0),
            attack=getattr(player, "attack", 0),
            defense=getattr(player, "defense", 0),
            max_mana=getattr(player, "max_mana", 0),
            armor=getattr(player, "armor", 0.0),
            crit=getattr(player, "crit_chance", 0.0),
            dodge=getattr(player, "dodge_chance", 0.0),
            spell_power=getattr(player, "spell_power", 0.0),
            heal_power=getattr(player, "heal_power", 0.0),
        )

    def _delta_preview_from_snapshot(self, player, before):
        """Erzeugt Vorher→Nachher Zeilen nach einem Kauf (für die gesamte Menge)."""
        lines = []
        def add_stat(label, old, new, fmt=lambda x: str(x)):
            if new != old:
                lines.append(f"{label}: {fmt(old)} -> {fmt(new)}")

        add_stat("Max-HP", before["max_hp"], getattr(player, "max_hp", 0), str)
        add_stat("ATK", before["attack"], getattr(player, "attack", 0), str)
        add_stat("DEF", before["defense"], getattr(player, "defense", 0), str)
        add_stat("Max-Mana", before["max_mana"], getattr(player, "max_mana", 0), str)
        add_stat("Rüstung", before["armor"], getattr(player, "armor", 0.0), lambda x: f"{int(round(x*100))}%")
        add_stat("Krit", before["crit"], getattr(player, "crit_chance", 0.0), lambda x: f"{int(round(x*100))}%")
        add_stat("Ausweichen", before["dodge"], getattr(player, "dodge_chance", 0.0), lambda x: f"{int(round(x*100))}%")
        add_stat("Zauberkraft", before["spell_power"], getattr(player, "spell_power", 0.0), lambda x: f"{x:.2f}")
        add_stat("Heilbonus", before["heal_power"], getattr(player, "heal_power", 0.0), lambda x: f"{x:.2f}")
        return lines
