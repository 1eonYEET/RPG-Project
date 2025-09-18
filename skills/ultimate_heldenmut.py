# skills/ultimate_heldenmut.py
from skills.skill import Skill

class Heldenmut(Skill):
    """
    Einmal pro Kampf: Großer, dauerhafter Kampf-Buff bis zum Ende des Kampfes.
    (Kein Runden-Timer nötig.)
    """
    def __init__(self):
        super().__init__(
            "Heldenmut",
            mana_cost=12,
            description="+20 ATK und +10 DEF bis zum Ende des Kampfes (einmal pro Kampf)."
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
        user.attack += 20
        user.defense += 10

        self.used_in_combat = True
        self._last_combat_id = getattr(user, "_combat_id", self._last_combat_id)

        logger.log(f"⚔️ {user.name} ruft {self.get_name()}! +20 ATK und +10 DEF bis zum Ende des Kampfes!")
