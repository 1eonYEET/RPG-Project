# skills/ultimate_toedlicher_schlag.py
from skills.skill import Skill

class ToedlicherSchlag(Skill):
    """
    Einmal pro Kampf: Garantierter Krit (2x) + 50% Bonus – insgesamt ca. 3x Basis-Nahkampfschaden.
    Trifft sicher (ignoriert Ausweichen), Schaden wird nach Rüstung reduziert.
    """
    def __init__(self):
        super().__init__(
            "Tödlicher Schlag",
            mana_cost=10,
            description="Garantierter Krit (+100%) +50% Bonus (≈3x Schaden), einmal pro Kampf."
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
        base = max(0, user.attack - target.defense)
        raw = int(base * 3)  # 2x (Crit) + 50% Bonus  => ~3x
        # Rüstungsreduktion anwenden (mag kein Ausweichen)
        mitigated = max(0, int(raw * (1.0 - getattr(target, "armor", 0.0))))
        target.receive_damage(mitigated)

        self.used_in_combat = True
        self._last_combat_id = getattr(user, "_combat_id", self._last_combat_id)

        logger.log(f"🗡️ {user.name} setzt {self.get_name()} ein! {target.name} erleidet {mitigated} Schaden (garantierter Krit).")
