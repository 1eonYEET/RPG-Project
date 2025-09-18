from abc import ABC, abstractmethod
import random


class Character(ABC):
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

        # Kampfstats (Startwerte für generische Charaktere)
        self.armor = 0.0          # Prozentuale Schadensreduktion (0.0–0.8)
        self.crit_chance = 0.0    # Wahrscheinlichkeit für kritischen Treffer (0.0–1.0)
        self.dodge_chance = 0.0   # Wahrscheinlichkeit für Ausweichen (0.0–0.6)

    def is_alive(self) -> bool:
        return self.hp > 0

    def receive_damage(self, amount: int):
        """Schaden nach Armor-Reduktion anwenden."""
        effective = self._apply_armor(amount)
        self.hp = max(0, self.hp - effective)

    def _apply_armor(self, amount: int) -> int:
        """Armor reduziert Schaden (max. 80%), mindestens 1 Schaden bleibt."""
        reduction = min(max(self.armor, 0.0), 0.8)
        reduced = int(round(amount * (1 - reduction)))
        return max(1, reduced)

    def attempt_attack(self, target: "Character", base_damage: int, logger, label: str = "Angriff"):
        """
        Angriff mit Dodge, Crit und Armor-Reduktion:
        1. Ziel weicht aus → 0 Schaden
        2. Crit? → doppelter Schaden
        3. Armor reduziert den Schaden
        """
        # Ausweichen
        if random.random() < min(max(target.dodge_chance, 0.0), 0.6):
            logger.log(f"🌀 {target.name} weicht {label} aus! Kein Schaden.")
            return

        # Kritischer Treffer
        crit = random.random() < min(max(self.crit_chance, 0.0), 1.0)
        raw_damage = base_damage * (2 if crit else 1)

        if crit:
            logger.log(f"💥 Kritischer Treffer von {self.name}!")

        effective_for_log = target._apply_armor(raw_damage)
        logger.log(f"⚔️ {self.name} trifft {target.name} für {effective_for_log} Schaden.")

        target.receive_damage(raw_damage)

    @abstractmethod
    def take_turn(self, opponent: "Character", logger):
        pass
