# skills/ultimate_arkaner_sturm.py
from skills.skill import Skill

class VampireGrandmaster(Skill):
    """
    Einmal pro Kampf: Massiver magischer Schaden. Ignoriert physische DEF
    und (für Klarheit) auch Rüstung – konzentrierter Zauber.
    """
    def __init__(self):
        super().__init__(
            "Vampir Großmeister",
            mana_cost=13,
            description="Erhöhe Permanent die Max HP (einmal pro Kampf)."
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
        # Erhöht Max HP um 5 Punkte
        bonus = 5
        user.add_max_health(bonus)

        self.used_in_combat = True
        self._last_combat_id = getattr(user, "_combat_id", self._last_combat_id)

        logger.log(f"🌩️ {user.name} entfesselt {self.get_name()}! {user.name} erhöht seine Max HP um {bonus} Punkte!")
