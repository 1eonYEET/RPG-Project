# skills/piercing_strike.py
from skills.skill import Skill

class PiercingStrike(Skill):
    def __init__(self):
        super().__init__(
            "Durchdringender Schlag",
            mana_cost=4,
            description="Physischer Angriff, der 25% der gegnerischen Verteidigung ignoriert."
        )

    def use(self, user, target, logger):
        effective_def = max(0, int(target.defense * 0.75))
        base = max(0, user.attack + 5 - effective_def)
        damage = base
        logger.log(f"🗡️ {user.name} setzt {self.get_name()} ein und verursacht {damage} Schaden (DEF teils ignoriert)!")
        target.receive_damage(damage)
