# skills/ultimate_unzerstoerbar.py
from skills.skill import Skill

class Unzerstoerbar(Skill):
    """
    Einmal pro Kampf: Heilt sofort 40% der Max-HP und setzt die Rüstung auf das Cap (80%).
    Tipp: Der Effekt hält für den gesamten Kampf (keine Runden-Dauerverwaltung nötig).
    """
    def __init__(self):
        super().__init__(
            "Unzerstörbar",
            mana_cost=12,
            description="Heilt 40% HP und setzt Rüstung auf 80% (einmal pro Kampf)."
        )
        self.used_in_combat = False
        self._last_combat_id = None

    def _soft_reset(self, user):
        cid = getattr(user, "_combat_id", None)
        if cid is not None and cid != self._last_combat_id:
            self.used_in_combat = False

    def use(self, user, target, logger):
        self._soft_reset(user)
        if self.used_in_combat:
            logger.log(f"{user.name} kann {self.get_name()} nur einmal pro Kampf nutzen!")
            return
        if user.mana < self.mana_cost:
            logger.log(f"Nicht genug Mana für {self.get_name()}! ({user.mana}/{self.mana_cost})")
            return

        user.mana -= self.mana_cost
        heal = max(0, int(user.max_hp * 0.40))
        user.hp = min(user.max_hp, user.hp + heal)
        user.armor = max(user.armor, 0.80)  # Cap sicherstellen
        self.used_in_combat = True
        self._last_combat_id = getattr(user, "_combat_id", self._last_combat_id)

        logger.log(f"🛡️ {user.name} nutzt {self.get_name()}! Heilt {heal} HP und setzt Rüstung auf 80%.")
