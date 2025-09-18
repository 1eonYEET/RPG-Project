# skills/ultimate_arkaner_sturm.py
from skills.skill import Skill

class ArkanerSturm(Skill):
    """
    Einmal pro Kampf: Massiver magischer Schaden. Ignoriert physische DEF
    und (für Klarheit) auch Rüstung – konzentrierter Zauber.
    """
    def __init__(self):
        super().__init__(
            "Arkaner Sturm",
            mana_cost=15,
            description="Massiver magischer Schaden, ignoriert Verteidigung & Rüstung (einmal pro Kampf)."
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
        damage = 50 + int(getattr(user, "spell_power", 0.0) * 20)
        # Ignoriert DEF & Rüstung
        target.receive_damage(damage)

        self.used_in_combat = True
        self._last_combat_id = getattr(user, "_combat_id", self._last_combat_id)

        logger.log(f"🌩️ {user.name} entfesselt {self.get_name()}! {target.name} erleidet {damage} magischen Schaden!")
