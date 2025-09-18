from battle.battle_manager import BattleManager
from messaging.console_notifier import ConsoleNotifier
from game.wave_manager import WaveManager
from characters.archetypes import Tank, Assassin, Mage, Knight
from systems.shop import Shop
from systems.run_tracker import RunTracker, RunRecord
from datetime import datetime

class GameLoop:
    def __init__(self):
        self.notifier = ConsoleNotifier()
        self.player = self._choose_class()
        self.player.kills = 0
        self.wave_manager = WaveManager()
        self.shop = Shop()

    def _choose_class(self):
        print("Wähle deine Klasse:")
        print("1. 🛡️ Tank   – mehr HP & Rüstung, schwächerer Dodge/DMG, besseres Heilen")
        print("2. 🗡️ Assassin – höherer DMG, Dodge & Crit, weniger HP")
        print("3. 🔮 Mage    – mehr Mana, effektivere Zauber")
        print("4. ⚔️ Knight  – ausgewogener Mix")

        choice = input("Deine Wahl: ")
        name = input("Gib deinem Helden einen Namen: ") or "Held"

        if choice == "1":
            return Tank(name)
        elif choice == "2":
            return Assassin(name)
        elif choice == "3":
            return Mage(name)
        else:
            return Knight(name)  # Default

    def start(self):
        self.notifier.notify("🏟️ ARENA-MODUS: Endlose Kampfwellen!")
        self.notifier.notify(f"🧙 {self.player.name} ({getattr(self.player, 'archetype','')}) "
                             f"→ HP:{self.player.hp} ATK:{self.player.attack} DEF:{self.player.defense}")

        while self.player.is_alive():
            enemy = self.wave_manager.next_enemy()
            self.notifier.notify(f"\n🌊 Neue Welle: {self.wave_manager.wave_number}")
            self.notifier.notify(f"Gegner erscheint: {enemy.name} (HP:{enemy.hp}, ATK:{enemy.attack}, DEF:{enemy.defense})")

            battle = BattleManager(self.player, enemy, self.notifier)
            battle.start()

            if not self.player.is_alive():
                self.notifier.notify("\n☠️ Du wurdest besiegt...")
                break

            if getattr(enemy, "is_boss", False):
                self.wave_manager.boss_defeated_increase_tier()
                self.notifier.notify(f"🔼 Die Gegner werden stärker! (Tier {self.wave_manager.tier})")

            self._post_fight_recovery()

            if self.wave_manager.wave_number % 5 == 0:
                # ⬇️ Tier an Shop geben (für Preisfaktor)
                self.shop.open(self.player, self.notifier, tier=self.wave_manager.tier)

        self.notifier.notify(f"\n💀 Endstand: Du hast {self.wave_manager.wave_number} Wellen überlebt.")

        tracker = RunTracker()
        rec = RunRecord(
            name=getattr(self.player, "name", "Spieler"),
            klass=getattr(self.player, "archetype", "Unbekannt"),
            gold=int(getattr(self.player, "gold", 0)),
            level=int(getattr(self.player, "level", 1)),
            kills=int(getattr(self.player, "kills", 0)),
            dt=datetime.utcnow().isoformat(timespec="seconds")
        )
        tracker.log_run(rec)
        self.notifier.notify("📝 Run gespeichert (data/runs.jsonl).")

    def _post_fight_recovery(self):
        """Zwischen den Wellen: KEINE HP-Heilung mehr. Nur Mana voll."""
        before = getattr(self.player, "mana", 0)
        self.player.mana = self.player.max_mana
        gained = self.player.mana - before
        # rein informativ, damit es klar sichtbar ist
        self.notifier.notify(
            f"🔷 Mana aufgefüllt (+{gained}). "
            f"HP bleiben bei {self.player.hp}/{self.player.max_hp}."
        )
